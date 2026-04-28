import pandas as pd
import pytest
from metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


# --- attrition_rate ---

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    assert attrition_rate(df) == 50.0


def test_attrition_rate_all_stay():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3],
        "attrition": ["No", "No", "No"],
    })
    assert attrition_rate(df) == 0.0


def test_attrition_rate_all_leave():
    df = pd.DataFrame({
        "employee_id": [1, 2],
        "attrition": ["Yes", "Yes"],
    })
    assert attrition_rate(df) == 100.0


# --- attrition_by_department ---

def test_attrition_by_department_columns():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "department": ["Sales", "Sales", "HR", "HR"],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_values():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "department": ["Sales", "Sales", "HR", "HR"],
        "attrition": ["Yes", "Yes", "No", "No"],
    })
    result = attrition_by_department(df)
    # Sales: 2/2 = 100%, HR: 0/2 = 0%, sorted descending by attrition_rate
    assert result.iloc[0]["department"] == "Sales"
    assert result.iloc[0]["attrition_rate"] == 100.0
    assert result.iloc[1]["department"] == "HR"
    assert result.iloc[1]["attrition_rate"] == 0.0


# --- attrition_by_overtime ---

def test_attrition_by_overtime_columns():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3],
        "overtime": ["Yes", "Yes", "No"],
        "attrition": ["Yes", "Yes", "No"],
    })
    result = attrition_by_overtime(df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_values():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "overtime": ["Yes", "Yes", "No", "No"],
        "attrition": ["Yes", "Yes", "No", "No"],
    })
    result = attrition_by_overtime(df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]
    assert yes_row["attrition_rate"] == 100.0
    assert no_row["attrition_rate"] == 0.0


# --- average_income_by_attrition ---

def test_average_income_by_attrition_columns():
    df = pd.DataFrame({
        "attrition": ["Yes", "No"],
        "monthly_income": [4000.0, 6000.0],
    })
    result = average_income_by_attrition(df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_values():
    df = pd.DataFrame({
        "attrition": ["Yes", "Yes", "No", "No"],
        "monthly_income": [4000.0, 6000.0, 5000.0, 7000.0],
    })
    result = average_income_by_attrition(df)
    yes_avg = result[result["attrition"] == "Yes"].iloc[0]["avg_monthly_income"]
    no_avg = result[result["attrition"] == "No"].iloc[0]["avg_monthly_income"]
    assert yes_avg == 5000.0
    assert no_avg == 6000.0


# --- satisfaction_summary ---

def test_satisfaction_summary_columns():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "job_satisfaction": [1, 1, 3, 3],
        "attrition": ["Yes", "Yes", "No", "No"],
    })
    result = satisfaction_summary(df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]


def test_satisfaction_summary_values():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "job_satisfaction": [1, 1, 3, 3],
        "attrition": ["Yes", "Yes", "No", "No"],
    })
    result = satisfaction_summary(df).reset_index(drop=True)
    # Sorted ascending by job_satisfaction: group 1 first, group 3 second
    assert result.iloc[0]["job_satisfaction"] == 1
    assert result.iloc[0]["attrition_rate"] == 100.0
    assert result.iloc[1]["job_satisfaction"] == 3
    assert result.iloc[1]["attrition_rate"] == 0.0


def test_satisfaction_summary_sorted_ascending():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "job_satisfaction": [4, 4, 2, 2],
        "attrition": ["No", "No", "Yes", "No"],
    })
    result = satisfaction_summary(df).reset_index(drop=True)
    assert list(result["job_satisfaction"]) == [2, 4]
