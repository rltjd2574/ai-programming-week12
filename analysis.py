from pathlib import Path

import pandas as pd

def 정제(data):
    data = data.copy()

    # 반과 과목 이름의 공백 정리
    data["반"] = data["반"].str.replace(r"\s+", "", regex=True)
    data["과목"] = data["과목"].str.strip()

    # 점수 결측 행 제거
    data = data.dropna(subset=["점수"])

    # 중복 행 제거
    data = data.drop_duplicates()

    # 점수 범위 검사
    data = data[data["점수"].between(0, 100)]

    return data


csv_path = Path(__file__).with_name("scores_2026.csv")
data = pd.read_csv(csv_path)

print(f"원본 행 수: {len(data)}")


def report_stage(name, before, after):
    removed = len(before) - len(after)
    print(f"{name}: 남은 행 수 {len(after)}, 제거된 행 수 {removed}")


# 점수가 결측값인 행 제거
after_missing = data.loc[data["점수"].notna()].copy()
report_stage("점수 결측 행 제거", data, after_missing)

# 반과 과목 이름의 앞뒤 공백 먼저 제거
after_missing["반"] = after_missing["반"].str.strip()
after_missing["과목"] = after_missing["과목"].str.strip()

# 모든 열의 값이 동일한 중복 행 제거
after_duplicates = after_missing.drop_duplicates().copy()
report_stage("중복 행 제거", after_missing, after_duplicates)

# 점수가 0 미만이거나 100을 초과하는 행 제거
score_in_range = after_duplicates["점수"].between(0, 100, inclusive="both")
cleaned = after_duplicates.loc[score_in_range].copy()
report_stage("점수 범위 초과 행 제거", after_duplicates, cleaned)

# 정제 후 반과 과목 종류 수 출력
print(f"반 종류 수: {cleaned['반'].nunique()}")
print(f"과목 종류 수: {cleaned['과목'].nunique()}")

# 정제된 데이터에서 반 이름과 과목명의 앞뒤 공백 확인
for column in ("반", "과목"):
    values = cleaned[column].astype("string")
    has_outer_whitespace = values.notna() & values.ne(values.str.strip())

    print(f"\n'{column}' 앞뒤 공백이 있는 값:")
    if has_outer_whitespace.any():
        whitespace_values = values.loc[has_outer_whitespace].map(repr)
        print(whitespace_values.to_string())
    else:
        print("없음")

# 이후 분석에 사용할 정제된 데이터
df = cleaned.copy()

# 과목이 '수학'인 행
math_df = df.loc[df["과목"] == "수학"].copy()
print("과목이 수학인 데이터:")
print(math_df)
print(f"행 개수: {len(math_df)}")

# 반이 '1반'이고 점수가 90점 이상인 행
class1_high_score_df = df.loc[
    (df["반"] == "1반") & (df["점수"] >= 90)
].copy()
print("\n1반이면서 점수가 90점 이상인 데이터:")
print(class1_high_score_df)
print(f"행 개수: {len(class1_high_score_df)}")

# 반별 평균 점수
class_average = df.groupby("반")["점수"].mean()
print("반별 평균 점수:")
print(class_average.to_frame(name="평균 점수"))

# 과목과 반별 평균 점수
subject_class_average = df.groupby(["과목", "반"])["점수"].mean()
print("\n과목과 반별 평균 점수:")
print(subject_class_average.to_frame(name="평균 점수"))

def 반별평균(df):
    return df.groupby("반")["점수"].agg(
        ["count", "mean", "median", "max"]
    ).round(2)


print("반별 통계:")
print(반별평균(df))

print("\n1반 통계:")
print(반별평균(df).loc["1반"])
# 합계 검증
sum_by_class = df.groupby("반")["점수"].sum().sum()
sum_direct = df["점수"].sum()

print("\n합계 검증:")
print("반별 합계의 합:", sum_by_class)
print("전체 점수 합계:", sum_direct)

# 개수 검증
count_by_class = df.groupby("반")["점수"].count().sum()
count_direct = len(df)

print("\n개수 검증:")
print("반별 인원수의 합:", count_by_class)
print("전체 데이터 행 수:", count_direct)

# 스팟 검증: 1반 수학 점수
math_1 = df.loc[
    (df["반"] == "1반") & (df["과목"] == "수학"),
    "점수"
]

direct_mean = math_1.mean()
group_mean = df.groupby(["과목", "반"])["점수"].mean().loc[("수학", "1반")]

print("\n스팟 검증:")
print("1반 수학 점수 직접 계산 평균:", direct_mean)
print("그룹화 결과 평균:", group_mean)
print("직접 계산한 점수 합계:", math_1.sum())
print("해당 인원수:", len(math_1))

# mini.csv 손계산 결과와 코드 결과 비교
미니 = 정제(pd.read_csv("mini.csv"))

print("\n미니 데이터 정제 결과:")
print(미니)

print("\n미니 데이터 반별 평균:")
print(반별평균(미니))