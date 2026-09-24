from pathlib import Path
from ..domain.family import Family
from ..domain.parameter import Parameter

_CANONICAL={
 "c11c_geometric_waves_v1":("geometric","Geometric Waves","Harmonic loom / liquid architecture.","wave interference; tension/release",["wave","phase","amplitude","morph","polygon_order","rational_frequency","layer_count","layer_offsets","scale","palette","palette_anchor","color_phase","loop_cycles"]),
 "c11c_fractal_bloom_v1":("fractal","Fractal Bloom","Bioluminescent mycelium / neural branching / microscopic universe.","z(n+1)=z(n)^2+c; radial nucleus; controlled zoom",["julia_constant","detail","branching","orbit_trap","domain_warp","warp_strength","zoom","depth_layers","organic_pulse","color_phase","color_diversity","palette","grammar"]),
 "c11c_sacred_symmetry_v1":("kaleidoscope","Sacred Symmetry","Generative astrolabe / celestial mechanism.","radial symmetry; concentric rings; clockwork precision",["symmetry_order","ring_count","rotation_phase","rotation_speed","gear_count","gear_ratio","angular_spacing","radial_scale","layer_offsets","palette","palette_anchor"]),
 "c11c_living_particles_v1":("particle_flow","Living Particles","Magnetic dust / ink in fluid.","density; flow; attractors; eddies; collision; trails",["particle_count","density","flow","attractors","eddies","collisions","trail_amount","trail_persistence","particle_scale","motion_strength","phase","palette"]),
 "c11c_invisible_forces_v1":("vector_field","Invisible Forces","Solar wind / gravitational topography / field traces.","TOPOGRAPHIC_BASIN; traces; pulse",["field_config","basin","trace_count","pulse_speed","field_phase","trace_curvature","field_intensity","flow","palette","palette_mode"]),
}

class FamilyRegistry:
    def __init__(self,ctx,introspector): self.ctx=ctx; self.introspector=introspector
    def load(self):
        out=[]; proto=self.ctx.paths.prototypes
        names=set(_CANONICAL)
        if proto.exists(): names |= {d.name for d in proto.glob("c11c_*_v1") if d.is_dir()}
        for fid in sorted(names):
            if fid in _CANONICAL: out.append(self._canonical(fid))
            else: out.append(self._dynamic(fid))
        return out
    def _canonical(self,fid):
        tech,art,desc,meta,params=_CANONICAL[fid]; folder=self.ctx.paths.family_dir(fid); launcher=folder/"run_prototype.ps1"; shader=next(iter(folder.glob("*.gdshader")),None) if folder.exists() else None; scene=next(iter(folder.glob("*.tscn")),None) if folder.exists() else None
        plist=[Parameter(x,x.replace("_"," ").title(),"unknown","SEED_DERIVED",source="canonical-family-matrix",family=fid) for x in params]
        plist=self._merge_script_params(fid,plist)
        grams=set(self.introspector.catalog.grammar_names.get(tech,set()))
        if fid=="c11c_fractal_bloom_v1": grams |= {"RADIAL BLOOM","DENDRITIC TUNNEL","SPIRAL FRACTAL","FRACTAL FILIGREE","NESTED WORLDS"}
        if fid=="c11c_invisible_forces_v1": grams.add("TOPOGRAPHIC_BASIN")
        pals=set(self.introspector.catalog.palette_names.get(tech,set()))
        caps=set(self.introspector.catalog.scripts.get(str(launcher),type("C",(),{"parameters":{}})()).parameters)
        return Family(fid,tech,art,fid,desc,meta,sorted(grams),sorted(pals),plist,launcher,shader,scene,caps)
    def _dynamic(self,fid):
        folder=self.ctx.paths.family_dir(fid); launcher=folder/"run_prototype.ps1"; tech=fid.removeprefix("c11c_").removesuffix("_v1"); art=tech.replace("_"," ").title(); plist=self._merge_script_params(fid,[]); return Family(fid,tech,art,fid,"Runtime-discovered C11-C family.","Discovered from backend.",[],[],plist,launcher,None,None,set(self.introspector.catalog.scripts.get(str(launcher),type("C",(),{"parameters":{}})()).parameters))
    def _merge_script_params(self,fid,plist):
        path=self.ctx.paths.family_dir(fid)/"run_prototype.ps1"; known={p.id for p in plist}; cap=self.introspector.catalog.scripts.get(str(path))
        if cap:
            for pid,typ in cap.parameters.items():
                if pid.lower() in {"seed","help","apply","nosound","silent","nofooter","force","grammar"}: continue
                if pid not in known: plist.append(Parameter(pid,pid.replace("_"," ").title(),typ,"USER_CONFIGURABLE",source="launcher-introspection",family=fid))
        for shader,ums in self.introspector.catalog.shader_uniforms.items():
            if fid in Path(shader).parent.name:
                for pid,typ in ums.items():
                    if not any(p.id==pid for p in plist): plist.append(Parameter(pid,pid.replace("_"," ").title(),typ,"BACKEND_EFFECTIVE",source="shader-uniform",family=fid))
        return plist
