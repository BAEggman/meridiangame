export const CONFIG = {
  "label": "게임 설정 · 임상 효과를 예측하는 값이 아님",
  "debug": false,
  "hours_per_day": 12,
  "cost_needle": 1, "cost_book": 1, "cost_exam": 1, "cost_move": 1,
  "move_installed": 0.5,
  "fit_base": 0.5, "fit_step": 0.2, "fit_min": 0.6,
  "pair_ratio": 0.3, "acute_ratio": 0.3, "p_shared_clue": 0,
  "shared_clue_note": "肺·大腸 是動所生에 공통 원문 문구 미확인. 다른 일반 주치를 진단 단서로 전용하지 않음.",
  "variant_ratio_min": 0, "variant_ratio_max": 0,
  "constraint_note": "교재에서 임부 침 금기 미확인. 검증 전 비활성.",
  "base_patients": 4, "max_patients": 4,
  "leave_nights": 3, "p_transfer": 0.5,
  "physician_capacity": 3, "physician_hours": 12,
  "quotas": {"theme":0.5,"draft":0.2,"due":0.2,"fresh":0.1},
  "install_gap_hours": 20, "reask_after_items": 3,
  "interval_first": 1, "mult": 2, "max_days": 60,
  "hit_radius": 18,
  "regions": {"hand":["arm"],"arm":["hand","chest"],"chest":["arm","back","abdomen"],"back":["chest","abdomen"],"abdomen":["chest","back","leg"],"leg":["abdomen","foot"],"foot":["leg"]},
  "region_labels": {"hand":"손","arm":"팔","chest":"가슴","back":"등","abdomen":"배","leg":"다리","foot":"발"},
  "fit": {"yuanluo":{"first":0.2,"pair":0.2,"single":-0.2,"chronic":0.2,"acute":-0.2},"shumu":{"organ":0.2,"chronic":0.2,"acute":0},"saam":{"match":0.2,"mismatch":-0.2}},
  "source": "사용자 v2 지시서 §2·3·6·8. 비용은 §2·3의 針당 비용과 실제 혈 구역 순회 기준. 최초 노출은 무힌트로 세지 않음."
}
;
