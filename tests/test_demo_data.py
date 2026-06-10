from demo_data import build_demo_bundle


def test_demo_bundle_supports_command_center_storyline():
    bundle = build_demo_bundle()

    assert len(bundle.monthly_trend["month"].drop_duplicates()) == 4
    assert {"risk_score", "review_score", "priority_score"}.issubset(bundle.monthly_trend.columns)
    assert len(bundle.quadrant) == 4
    assert bundle.quadrant["priority_score"].max() >= 200
    assert set(bundle.risk_sources["source"]) >= {"申報落差", "居家附近", "工時不足"}
    assert set(bundle.talk_tracks["employee"]) >= {"B001 陳南院", "C001 張北診"}


def test_demo_app_copy_is_positioned_for_hr_resume_review():
    app_source = open("demo_app.py", encoding="utf-8").read()

    assert "給 HR 看的外勤稽核作品集" in app_source
    assert "HR 團隊常見痛點" in app_source
    assert "關鍵技術" in app_source
    assert "01 問題總覽" in app_source
