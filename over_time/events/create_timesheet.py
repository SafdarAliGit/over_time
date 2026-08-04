import frappe
from datetime import datetime, timedelta, time
from frappe.query_builder import DocType
from frappe.utils import get_datetime

from .holiday_work import get_holiday_work


@frappe.whitelist()
def create_timesheet(**args):
    start_date = args.get("start_date")
    end_date = args.get("end_date")

    frappe.enqueue(
        _create_timesheets_job,
        queue="long",
        timeout=1500,
        job_name=f"create_timesheets_{start_date}_{end_date}",
        start_date=start_date,
        end_date=end_date,
        user=frappe.session.user,
    )

    return frappe.msgprint(
        f"Timesheet creation for {start_date} to {end_date} has been queued and will run in the background. "
        "You will be notified once it completes."
    )


def _create_timesheets_job(start_date, end_date, user):
    try:
        create_timesheets_for_employees(start_date, end_date)
        frappe.publish_realtime(
            "timesheet_creation_complete",
            {
                "success": True,
                "message": f"Timesheets created successfully for {start_date} to {end_date}.",
            },
            user=user,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Create Timesheet Background Job Failed")
        frappe.publish_realtime(
            "timesheet_creation_complete",
            {
                "success": False,
                "message": f"Timesheet creation failed for {start_date} to {end_date}. Check Error Log for details.",
            },
            user=user,
        )


def get_shift_window(shift, in_time):
    """
    Return (shift_start, shift_end) as real datetimes anchored to the
    check-in date. Handles shifts that end on the next calendar day.
    """
    shift_type = frappe.get_cached_doc("Shift Type", shift)
    if shift_type.start_time is None or shift_type.end_time is None:
        return None, None

    base_date = in_time.date()
    shift_start = datetime.combine(base_date, (datetime.min + shift_type.start_time).time())
    shift_end = datetime.combine(base_date, (datetime.min + shift_type.end_time).time())

    # Overnight shift (e.g. 22:00 -> 06:00)
    if shift_end <= shift_start:
        shift_end += timedelta(days=1)

    return shift_start, shift_end


def over_time(shift, in_time, out_time):
    """
    Overtime = time worked beyond the shift end.
    Uses full datetimes so a check-out after midnight is handled correctly.
    """
    if not (shift and in_time and out_time):
        return 0.0

    in_time = get_datetime(in_time)
    out_time = get_datetime(out_time)

    shift_start, shift_end = get_shift_window(shift, in_time)
    if not shift_start:
        return 0.0

    # Check-out recorded before check-in means it rolled over to the next day
    if out_time < in_time:
        out_time += timedelta(days=1)

    return (out_time - shift_end).total_seconds() / 3600


def create_timesheets_for_employees(start_date, end_date):
    settings = get_over_time_settings()
    if "error" in settings:
        return

    consider_over_time = settings["consider_over_time"]
    department = [item.department for item in settings["department"]]
    award_on_over_time = settings["award_on_over_time"]
    award_hours = settings["award_hours"]
    on_over_time_hours = settings["on_over_time_hours"]

    if not department:
        return

    Attendance = DocType("Attendance")
    query = (
        frappe.qb.from_(Attendance)
        .select(
            Attendance.in_time,
            Attendance.out_time,
            Attendance.department,
            Attendance.name,
            Attendance.employee,
            Attendance.shift,
            Attendance.working_hours,
            Attendance.attendance_date,
        )
        .where(
            (Attendance.attendance_date >= start_date)
            & (Attendance.attendance_date <= end_date)
            & (Attendance.department.isin(department))
            & Attendance.in_time.isnotnull()
            & Attendance.out_time.isnotnull()
            & (Attendance.docstatus == 1)
        )
        .orderby(Attendance.employee)
        .orderby(Attendance.attendance_date)
    )

    attendance_data = query.run(as_dict=True)

    # Group attendances by employee
    employee_attendances = {}
    for record in attendance_data:
        if not timesheet_not_present(record.employee, start_date, end_date):
            continue

        overtime = over_time(record.shift, record.in_time, record.out_time)

        if get_holiday_work(settings["holiday_list"], record.attendance_date):
            overtime = record.working_hours or 0

        if overtime <= consider_over_time:
            continue

        if award_on_over_time and overtime >= on_over_time_hours:
            overtime += award_hours

        record["over_time"] = overtime
        employee_attendances.setdefault(record.employee, []).append(record)

    # Create a Timesheet for each employee
    for employee, attendances in employee_attendances.items():
        sum_over_time = 0

        timesheet_doc = frappe.new_doc("Timesheet")
        timesheet_doc.employee = employee

        for attendance in attendances:
            timesheet_detail = timesheet_doc.append("time_logs", {})
            timesheet_detail.activity_type = "Execution"
            timesheet_detail.from_time = attendance["in_time"]
            timesheet_detail.to_time = attendance["out_time"]
            timesheet_detail.custom_checkin_time = attendance["in_time"]
            timesheet_detail.checkout_time = attendance["out_time"]
            timesheet_detail.custom_modified_checkin_time = 0
            timesheet_detail.over_time = float(attendance["over_time"])
            timesheet_detail.custom_attendance = attendance["name"]
            sum_over_time += timesheet_detail.over_time

        timesheet_doc.custom_over_time = sum_over_time
        timesheet_doc.save()
        frappe.db.commit()


def timesheet_not_present(employee, start_date, end_date):
    """
    Check if a Timesheet record exists for the given employee, start_date and end_date.
    Returns True if no record is found, False otherwise.
    """
    Timesheet = DocType("Timesheet")

    query = (
        frappe.qb.from_(Timesheet)
        .select(Timesheet.name)
        .where(
            (Timesheet.employee == employee)
            & (Timesheet.start_date >= start_date)
            & (Timesheet.end_date <= end_date)
        )
        .limit(1)
    )

    return not query.run(as_dict=True)


def get_over_time_settings():
    """
    Fetch and return the data from the Over Time Settings single doctype.
    """
    try:
        settings = frappe.get_single("Over Time Settings")

        return {
            "consider_over_time": settings.consider_over_time or 0,
            "department": settings.department or [],
            "holiday_list": settings.holiday_list,
            "award_on_over_time": settings.award_on_over_time,
            "award_hours": settings.award_hours or 0,
            "on_over_time_hours": settings.on_over_time_hours or 0,
        }

    except frappe.DoesNotExistError:
        return {"error": "Over Time Settings single doctype is not configured."}


def calculate_over_time(in_time):
    """
    Calculate overtime: 0.5 if in_time <= 09:30 else 0.
    Accepts string "dd/mm/yyyy HH:MM" or datetime object.
    """
    try:
        if isinstance(in_time, str):
            in_time_obj = datetime.strptime(in_time, "%d/%m/%Y %H:%M")
        elif isinstance(in_time, datetime):
            in_time_obj = in_time
        else:
            return 0.0

        check_time = datetime.combine(in_time_obj.date(), time(9, 30))

        return 0.5 if in_time_obj <= check_time else 0.0

    except Exception:
        return 0.0



def normalize_in_time(in_time):
    """
    If in_time <= 09:30, return datetime set to 09:00 of the same day.
    Otherwise, return in_time unchanged.
    """
    if not isinstance(in_time, datetime):
        return in_time

    check_time = datetime.combine(in_time.date(), time(9, 30))

    if in_time <= check_time:
        return datetime.combine(in_time.date(), time(9, 0))

    return in_time

