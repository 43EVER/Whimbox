from whimbox.ui.ui_assets import *

# 能力配置界面，能力图标半径
ability_icon_radius = 50
# 能力配置界面，8个能力图标中心点
ability_icon_centers = [
    (1099, 277), (1192, 437), (1193, 627), (1099, 789),
    (587, 788), (493, 625), (493, 438), (587, 276)
]
# 净化能力配置图标中心点
battle_ability_centers = (228, 450)
# 跳跃能力配置图标中心点
jump_ability_center = (228, 625)


# hsv处理后的能力图标，用于匹配
ability_hsv_icons = [
    IconAbilityAnimal, 
    IconAbilityInsect, 
    IconAbilityFish, 
    IconAbilityFly, 
    IconAbilitySmall, 
    IconAbilityBig, 
    IconAbilityStick, 
    IconAbilityFlourish,
    IconAbilityShapeshifting,
]
jump_ability_hsv_icons = [IconAbilityFloat, IconAbilityWing]

ABILITY_NAME_ANIMAL = '动物清洁'
ABILITY_NAME_INSECT = '捕虫'
ABILITY_NAME_FISH = '钓鱼'
ABILITY_NAME_FLY = '滑翔'
ABILITY_NAME_SMALL = '变小'
ABILITY_NAME_BIG = '变大'
ABILITY_NAME_STICK = '黏黏爪'
ABILITY_NAME_FLOURISH = '芳间巡游'
ABILITY_NAME_SHAPESHIFTING = '化万相'

ABILITY_NAME_FLOAT = '漂浮'
ABILITY_NAME_WING = '悬羽'

icon_name_to_ability_name = {
    'IconAbilityAnimal': ABILITY_NAME_ANIMAL,
    'IconAbilityInsect': ABILITY_NAME_INSECT,
    'IconAbilityFish': ABILITY_NAME_FISH,
    'IconAbilityFly': ABILITY_NAME_FLY,
    'IconAbilitySmall': ABILITY_NAME_SMALL,
    'IconAbilityFloat': ABILITY_NAME_FLOAT,
    'IconAbilityWing': ABILITY_NAME_WING,
    'IconAbilityBig': ABILITY_NAME_BIG,
    'IconAbilityStick': ABILITY_NAME_STICK,
    'IconAbilityFlourish': ABILITY_NAME_FLOURISH,
    'IconAbilityShapeshifting': ABILITY_NAME_SHAPESHIFTING,
}