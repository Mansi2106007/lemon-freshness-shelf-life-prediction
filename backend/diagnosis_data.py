"""
diagnosis_data.py
------------------
Farmer-facing text for each class in config.CLASSES: a plain-language name,
whether it originates pre- or post-harvest, the likely cause, and concrete
field actions. Content is paraphrased from the findings/discussion/
conclusions of Botina A. et al. (2019), "Pre- and post-harvest factors that
affect the quality and commercialization of the Tahiti lime," Scientia
Horticulturae 257.

This is the single place to edit if the wording needs to change — both the
API (api/app.py) and any frontend rendering pull from here, so they can
never drift out of sync.
"""

DIAGNOSIS = {
    "healthy": {
        "label": "Healthy fruit",
        "stage": "none",
        "cause": (
            "No significant surface damage detected. Fruit like this held up "
            "best in the study when it was harvested carefully, disinfected, "
            "and moved into cold storage quickly."
        ),
        "actions": [
            "Keep doing what you're doing: gentle harvest handling and prompt cooling.",
            "Disinfect crates and tools between batches so healthy fruit doesn't pick up rot from others.",
        ],
    },
    "sunburn": {
        "label": "Sunburn / sunspot",
        "stage": "pre-harvest",
        "cause": (
            "Caused by too much direct sun on the fruit, either while it's still "
            "on the tree or after harvest if it's left uncovered. Shows up as "
            "pale or discolored patches, and in bad cases dry, hardened spots."
        ),
        "actions": [
            "Prune to open the canopy evenly rather than leaving fruit fully exposed on one side.",
            "Get harvested fruit into shade or covered transport quickly — don't let full crates sit in the sun.",
        ],
    },
    "scars": {
        "label": "Scarring",
        "stage": "pre-harvest",
        "cause": (
            "Scratches from wind, hail, or the fruit rubbing against thorns and "
            "branches. Young, small fruit are the most vulnerable, and the mark "
            "just gets more visible as the fruit grows."
        ),
        "actions": [
            "Put up windbreaks or curtains if your plot gets strong or gusty wind.",
            "Manage branch density near fruiting wood to cut down on thorn contact.",
        ],
    },
    "pest_damage": {
        "label": "Pest damage",
        "stage": "pre-harvest",
        "cause": (
            "Mites, thrips, or scale insects feeding on the peel, leaving a "
            "cork-like, stippled, or rough-textured patch."
        ),
        "actions": [
            "Scout regularly for citrus rust mite, aphids, and scale insects, especially in dry-season windows.",
            "Bring in integrated pest management before numbers build up rather than after damage shows.",
        ],
    },
    "yellowing": {
        "label": "Yellowing",
        "stage": "post-harvest",
        "cause": (
            "Loss of green color as chlorophyll breaks down during storage. This "
            "isn't ripening — Tahiti lime doesn't ripen after picking — it's "
            "degreening, and cold storage only slows it, it doesn't stop it."
        ),
        "actions": [
            "Cool fruit to around 10\u00b0C as soon as possible after harvest.",
            "If yellowing is a recurring problem, look into ethylene control alongside refrigeration.",
        ],
    },
    "dehydration": {
        "label": "Dehydration",
        "stage": "post-harvest",
        "cause": (
            "Moisture loss from storage or transport humidity that's too low, "
            "leaving the fruit shriveled, wrinkled, or unusually hard."
        ),
        "actions": [
            "Keep storage humidity close to 90% rather than letting it swing low.",
            "Use a wax coating or protective film to cut down on moisture loss in transit.",
        ],
    },
    "brown_spot": {
        "label": "Brown spot / browning",
        "stage": "post-harvest",
        "cause": (
            "Brown pigmentation on the peel, most often from chilling injury, "
            "disease, or just the fruit aging in storage."
        ),
        "actions": [
            "Avoid storing fruit colder than needed — chilling injury shows up as this same browning.",
            "Disinfect before storage and move fruit through the chain faster to limit aging-related browning.",
        ],
    },
    "mechanical_damage": {
        "label": "Mechanical damage",
        "stage": "post-harvest",
        "cause": (
            "Bruises, cuts, or oil-gland rupture (oleocellosis) from rough "
            "handling — drops, rubbing, or tight packing."
        ),
        "actions": [
            "Handle fruit gently at harvest and during sorting — avoid drops and rough tipping into crates.",
            "Check packing density; overly tight crates increase rubbing and bruising in transit.",
        ],
    },
    "microbial_damage": {
        "label": "Microbial / fungal damage",
        "stage": "post-harvest",
        "cause": (
            "Fungal rot — commonly Colletotrichum (anthracnose), Fusarium, "
            "Penicillium, or Alternaria — usually entering through an existing "
            "wound or a latent infection picked up in the field."
        ),
        "actions": [
            "Disinfect fruit (e.g. a brief diluted sodium hypochlorite rinse) and cool promptly after harvest.",
            "Keep packhouse surfaces and tools clean, and pull visibly infected fruit out of the line fast — it spreads to neighboring fruit quickly.",
        ],
    },
}


def get_diagnosis(class_name: str) -> dict:
    """Look up the farmer-facing info for a predicted class.

    Falls back to a safe default if an unrecognized class name is passed in
    (e.g. a model/config mismatch), so the API never crashes on this step.
    """
    return DIAGNOSIS.get(
        class_name,
        {
            "label": class_name.replace("_", " ").title(),
            "stage": "unknown",
            "cause": "No description available for this class yet.",
            "actions": ["Ask the team to add field guidance for this class."],
        },
    )
