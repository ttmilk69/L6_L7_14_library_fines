import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------
def test_returned_on_time():
    assert late_fine("student", 10, False) == 0


def test_unknown_member():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("alien", 5, False)


def test_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_faculty_on_time():
    assert late_fine("faculty", 30, False) == 0          # boundary: overdue == 0


def test_faculty_overdue():
    assert late_fine("faculty", 40, False) == 10


def test_student_boundary_14_days():
    assert late_fine("student", 14, False) == 0          # boundary: no fine


def test_student_overdue():
    assert late_fine("student", 20, False) == 12


def test_fine_below_cap():
    assert late_fine("guest", 20, False) == 30           # 6 * 5, not capped


def test_fine_exactly_200_not_capped_branch():
    assert late_fine("student", 114, False) == 200       # 100 * 2 = 200 (not > 200)


def test_fine_capped_at_200():
    assert late_fine("guest", 100, False) == 200


def test_damaged_book_surcharge():
    assert late_fine("student", 10, True) == 150


def test_damaged_and_overdue():
    assert late_fine("student", 20, True) == 162         # 12 + 150


def test_damaged_and_capped():
    assert late_fine("guest", 100, True) == 350          # 200 + 150


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True


def test_cannot_borrow_high_fine():
    assert can_borrow(1, 101, "student") is False


def test_fine_boundary_100_allowed():
    assert can_borrow(1, 100, "student") is True


def test_faculty_can_borrow():
    assert can_borrow(9, 0, "faculty") is True


def test_faculty_limit_reached():
    assert can_borrow(10, 0, "faculty") is False


def test_student_limit_reached():
    assert can_borrow(3, 0, "student") is False


def test_student_just_below_limit():
    assert can_borrow(2, 0, "guest") is True


# ---------- renewal_status ----------
def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(1, False, -1) == "overdue"


def test_renewal_success():
    assert renewal_status(1, False, 0) == "renewed"      # boundary: days_left == 0
