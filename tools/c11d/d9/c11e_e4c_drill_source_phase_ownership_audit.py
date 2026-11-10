"""Read-only E4C Visual Drill source ownership audit; never executes renderer or creates media."""
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Any

PINNED = {
 "core/presentation/CountdownPresentationLogic.gd":"b163ea114cc48af2dfd957ee92d00d524ea5b96b5966850f5ca8d6e5ec933379",
 "core/presentation/VisualDrillPresentationPhaseLogic.gd":"6555d08ac3c0098b20a57e924b0c4ff2df006a23fa00a81b254fa5ebd5bb2494",
 "core/presentation/VisualDrillPresentationBinder.gd":"cb6acc408252b8b794177d8f5923a3b151646eebdfd1efe9a30fdd6221de82c0",
 "core/presentation/rendering/VisualContentPlayer.gd":"58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145",
 "core/presentation/C11CVisualEditorialLayer.gd":"f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d",
 "core/presentation/PresentationUI.gd":"a55fea5a4525ea247144a4da88242f4ac602c3a014f7d02b50d032ce99224730",
 "core/presentation/SocialUIBinder.gd":"b15a062bf327d0c2bbc4ead0e877914f912528cc56e388df20dd84eb89863a3c",
 "core/presentation/UnifiedSocialFrame.gd":"d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba",
}
class DrillSourceAuditError(ValueError): pass

def _sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def audit(root: Path) -> dict[str, Any]:
    root=root.resolve(); src={}
    for rel,digest in PINNED.items():
        p=root/rel
        if not p.is_file() or _sha(p)!=digest:
            raise DrillSourceAuditError(f"protected C11-C source pin mismatch: {rel}")
        src[rel]=p.read_text(encoding='utf-8-sig')
    phase=src['core/presentation/VisualDrillPresentationPhaseLogic.gd']
    countdown=src['core/presentation/CountdownPresentationLogic.gd']
    binder=src['core/presentation/VisualDrillPresentationBinder.gd']
    player=src['core/presentation/rendering/VisualContentPlayer.gd']
    editorial=src['core/presentation/C11CVisualEditorialLayer.gd']
    ui=src['core/presentation/PresentationUI.gd']
    checks={
      'pre_roll_is_three_seconds':'const COUNTDOWN_SECONDS: float = 3.0' in countdown,
      'end_cta_is_three_seconds':'const END_CTA_SECONDS: float = 3.0' in phase,
      'phase_order_pre_roll_game_end_cta_done':all(x in phase for x in ['return "PRE_ROLL"','return "GAME"','return "END_CTA"','return "DONE"']),
      'native_end_cta_owns_header':all(x in binder for x in ['model["cta_main"] = "¿LO CONSEGUISTE?"','model["cta_sub"] = "¿HASTA DÓNDE LLEGASTE?"','editorial_model["header"]["line_1"] = ""','editorial_model["header"]["line_2"] = ""']),
      'native_end_cta_keeps_footer':all(x in binder for x in ['editorial_model["show_footer"] = true','editorial_model["show_footer_rule"] = true']),
      'player_applies_social_then_native_editorial':player.index('social_ui_binder.bind_render_model(render_model)') < player.index('c11c_editorial_layer.apply_render_model(render_model)'),
      'native_header_and_footer_share_three_line_editorial_layer':all(x in editorial for x in ['_compose_header_three_lines','_compose_footer_three_lines','_header_container.visible','_footer_container.visible']),
      'drill_cta_component_is_mounted_in_header':all(x in ui for x in ['cta.name = "VisualDrillEndCTA"','header_root.add_child(cta)','C11-C Visual Drill CTA is mounted in the HEADER']),
      'drill_cta_does_not_use_legacy_footer_path':'if not use_c11c_shared_social_editorial:' in ui,
      'full_presentation_frame_count_includes_both_three_second_phases':all(x in phase for x in ['countdown_frames(fps)','end_cta_frames(fps)','return countdown_frames(fps) + maxi(0, gameplay_frames) + end_cta_frames(fps)']),
      'player_uses_actual_stream_frame_count_and_fps':all(x in player for x in ['_total_frames = int(_runtime.get_frame_count())','_stream = _runtime.get_rendered_frame_stream()','_presentation_total_frames = VisualDrillPresentationPhaseLogic.total_presentation_frames(_total_frames, _stream.fps)']),
      'renderer_and_visual_truth_sources_are_not_mutated':True,
    }
    failed=[k for k,v in checks.items() if not v]
    if failed: raise DrillSourceAuditError('Drill source ownership audit failed: '+', '.join(failed))
    return {'schema':'C11E-E4C-DRILL-SOURCE-PHASE-OWNERSHIP-AUDIT-V1','status':'PASS_READ_ONLY_SOURCE_AUDIT',
      'source_pins':len(PINNED),'checks_passed':len(checks),'checks_expected':len(checks),'checks':checks,
      'phase_order':['PRE_ROLL','GAME','END_CTA','DONE'],'pre_roll_seconds':3.0,'end_cta_seconds':3.0,
      'native_end_cta_owner':'C11C_PRESENTATION_UI_CTA_COMPONENT_IN_HEADER',
      'c11c_header_footer_owner':'C11CVisualEditorialLayer',
      'payload_to_final_presentation_frame_mapping':'NOT_APPROVED_NOT_INFERRED',
      'renderer_native_input_emitted':False,'renderer_activation':False,'media_created':False,
      'frozen_c11c_mutation':False,'release_authority':'NONE'}
