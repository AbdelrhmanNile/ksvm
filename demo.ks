cpt leaf_color yellow/white/normal
cpt leaf_shape wilted/normal
cpt stem_shape thin/normal
cpt stem_color red/white/normal
cpt spikes_status dead/empty/normal
cpt spikes_color white/normal

if (leaf_color eq yellow) and (stem_shape eq thin) and (spikes_status eq dead) then nitrogen_deficiency
if (leaf_shape eq wilted) and (stem_color eq red) and (spikes_status eq empty) then leaf_rust
if (leaf_color eq white) and (stem_color eq white) and (spikes_color eq white) then powedery_mildew
if (nitrogen_deficiency eq true) and (leaf_rust eq true) and (powedery_mildew eq true) then all_are_true
if (nitrogen_deficiency eq true) or (leaf_rust eq true) or (powedery_mildew eq true) then at_least_one_is_true
