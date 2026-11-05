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


def test_faculty_overdue():
    # 40 - 30 = 10 days overdue * 1 = 10
    assert late_fine("faculty", 40, False) == 10


def test_student_overdue():
    # 20 - 14 = 6 days overdue * 2 = 12
    assert late_fine("student", 20, False) == 12


def test_fine_capped_at_200():
    # guest: 100 - 14 = 86 * 5 = 430 -> capped to 200
    assert late_fine("guest", 100, False) == 200


def test_damaged_book_surcharge():
    assert late_fine("student", 10, True) == 150


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True


def test_cannot_borrow_high_fine():
    assert can_borrow(1, 101, "student") is False


def test_faculty_can_borrow():
    assert can_borrow(5, 0, "faculty") is True


def test_student_limit_reached():
    assert can_borrow(3, 0, "student") is False


# ---------- renewal_status ----------
def test_renewal_denied_reservation():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"


def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"
