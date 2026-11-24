def test_mini_score_range():
    assert analysis.미니["점수"].between(0, 100).all()

import analysis


def test_cleaned_rows():
    assert len(analysis.df) == 100


def test_class_types():
    assert sorted(analysis.df["반"].unique()) == ["1반", "2반"]


def test_sum_check():
    assert (
        analysis.df.groupby("반")["점수"].sum().sum()
        == analysis.df["점수"].sum()
    )


def test_mini_average():
    assert analysis.반별평균(analysis.미니).loc["1반", "mean"] == 80.0

def test_mini_class_types():
    assert sorted(analysis.미니["반"].unique()) == ["1반", "2반"]

def test_cleaned_score_range():
    assert analysis.df["점수"].between(0, 100).all()