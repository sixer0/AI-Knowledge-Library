# BIM Modeling SOP

> For creating BimDown models from existing designs. Focuses on creation order, dependencies, and pitfalls.

## Core Principles

1. **Bottom-up**: lowest floor first
2. **Outside-in**: exterior walls → interior walls
3. **Skeleton first**: walls/slabs → doors/windows/spaces
4. **Validate frequently**: `bimdown build` + `bimdown render` after each element type
5. **One floor, then replicate**: complete typical floor → copy to others

## Element Creation Order

```
1. global/level.csv         ← MUST be first
2. global/grid.csv          ← recommended second
3. wall.csv + .svg          ← depends on level
   ├─ door.csv              ← depends on wall (host_id)
   ├─ window.csv            ← depends on wall (host_id)
   └─ opening.csv           ← depends on wall or slab
4. column.csv + .svg        ← independent
5. slab.csv + .svg          ← needs wall outline known
6. space.csv                ← needs walls enclosed (build computes boundary)
7. stair, ramp, railing     ← independent
8. ceiling, roof            ← roof on top floor only
9. structure_column, beam, structure_slab, foundation
10. MEP: duct/pipe/cable_tray/conduit, equipment, terminal
11. bimdown resolve-topology ← LAST for MEP
```

## Per-Element Guide

### level (`global/level.csv`)
Must be first. `elevation` = cumulative meters from ground (0). Basements negative. Directory name = level id (e.g., `lv-1`, `lv-B1`, `lv-R`).

**Pitfall**: using floor height instead of cumulative elevation.

### grid (`global/grid.csv`)
X-direction grids (vertical lines): `start_x = end_x`. Y-direction grids (horizontal): `start_y = end_y`. Extend 2–5m beyond building.

**Pitfall**: confusing X/Y — X-grids are vertical lines (constant x).

### wall (`lv-N/wall.csv` + `.svg`)
Most critical element. One wall = one straight line. Never split for doors/windows. Endpoints must align exactly at junctions — even 0.001m gap breaks space computation. `stroke-width` = `thickness` (CSV is source of truth).

**Order**: exterior → core → major interior → partitions. Render immediately after.

**Pitfalls**: forgetting `<g transform="scale(1,-1)">`, endpoints not aligned, splitting walls at doors.

### door (`lv-N/door.csv` — CSV only)
**Recommended**: use `host_x, host_y` (2D coordinate of door center) — `bimdown build` auto-resolves to nearest wall + position. Alternative: manual `host_id` + `position` (meters from wall start to center). Validate: `position ± width/2` within wall length. No overlaps on same wall.

**Before placing doors, write a room connectivity graph** (e.g., `Stair→Corridor→Office`, `Corridor→Meeting Room`). Each connection = one door. Verify every room traces back to a stair/elevator.

**Pitfalls**: missing connections (room inaccessible), host_x/host_y too far from any wall (>5cm).

### window (`lv-N/window.csv` — CSV only)
Same rules as door. **Always set `base_offset`** = sill height (standard 0.9m). Omitting it puts windows at floor level.

### slab (`lv-N/slab.csv` + `.svg`)
Polygon matching exterior wall outline. `function`: floor/roof. Account for shaft openings.

**Pitfall**: polygon not matching wall outline, forgetting openings.

### column (`lv-N/column.csv` + `.svg`)
SVG `<rect>` x,y = **corner** not center. For 0.5×0.5 column at origin: `x=-0.25, y=-0.25`. Round columns: `<circle cx= cy= r=>`.

**Pitfall**: using center coords for `<rect>` x,y.

### space (`lv-N/space.csv` — CSV only)
Seed point (x,y) inside enclosed room + `name`. `bimdown build` computes boundary.

**Pitfall**: seed point on/outside wall, room not fully enclosed.

### stair (`lv-N/stair.csv` + `.svg`)
SVG = plan projection path. CSV: `width`, `step_count`, `start_z`, `end_z` (offsets from level).

### curtain_wall, ceiling, roof
- Curtain wall: line element like wall, with `u_grid_count`/`v_grid_count`
- Ceiling: polygon, `height_offset` above level
- Roof: polygon, `roof_type` (flat/gable/hip/shed/mansard), `slope` in degrees. Top floor only.

### Structure (structure_column, beam, foundation)
- structure_column: like column but `structural_section_profile` supports i/t/l/c/cross shapes
- beam: spatial line, `start_z`/`end_z`, section profile (primary rect 0.3×0.6m, secondary 0.2×0.4m)
- foundation: geometry determines form — `<rect>`/`<circle>` = isolated, `<path>` = strip, `<polygon>` = raft

### MEP (duct, pipe, cable_tray, conduit)
Spatial line elements. `shape` (rect/round), `size_x`(/`size_y`), `system_type`, `start_z`/`end_z`. Align endpoints to create connections. Run `bimdown resolve-topology` after all MEP placed.

### equipment & terminal
Point elements. `equipment_type`: ahu, fcu, chiller, boiler, cooling_tower, fan, pump, transformer, panelboard, generator, water_heater, tank, other. `terminal_type`: supply_air_diffuser, return_air_grille, exhaust_air_grille, sprinkler_head, fire_alarm_device, light_fixture, power_outlet, data_outlet, plumbing_fixture, other.

## Multi-Story Efficiency

1. Complete typical floor (usually lv-2) → validate → copy CSV+SVG to other `lv-N/` dirs
2. IDs are level-scoped — same `w-1` in different levels = different elements
3. Modify non-standard floors: GF lobby, top floor mechanical/roof, basement parking

## Common Build Errors

| Error | Fix |
|-------|-----|
| Unconnected wall endpoint | Align endpoint coordinates exactly |
| Door/window out of bounds | Recalculate position or reduce width |
| Overlapping openings | Adjust positions on same wall |
| Space seed not enclosed | Move seed point inside or close wall gaps |
| Unknown column in CSV | Remove computed field from CSV |
| SVG ID not in CSV | Add CSV row or remove SVG element |

## Final Checklist

- [ ] `bimdown build` — zero warnings/errors
- [ ] `bimdown render` every floor — visually correct
- [ ] `bimdown info` — counts reasonable, no empty levels
- [ ] All rooms connected per connectivity graph (every room traces to stair/elevator via doors)
- [ ] Windows have `base_offset` set (sill height)
- [ ] Slabs cover full footprint per level
- [ ] MEP topology resolved (if applicable)
- [ ] `bimdown publish` — 3D preview URL provided
