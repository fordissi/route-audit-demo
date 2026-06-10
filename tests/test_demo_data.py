from demo_data import build_demo_bundle


def test_demo_bundle_supports_command_center_storyline():
    bundle = build_demo_bundle()

    assert len(bundle.monthly_trend["month"].drop_duplicates()) == 4
    assert {"risk_score", "review_score", "priority_score"}.issubset(bundle.monthly_trend.columns)
    assert len(bundle.quadrant) == 4
    assert bundle.quadrant["priority_score"].max() >= 200
    assert set(bundle.risk_sources["source"]) >= {"申報落差", "居家附近", "工時不足"}
    assert set(bundle.talk_tracks["employee"]) >= {"B001 陳南院", "C001 張北診"}
