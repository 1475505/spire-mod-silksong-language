package com.silksong.lang;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.evacipated.cardcrawl.modthespire.lib.SpireInitializer;
import com.megacrit.cardcrawl.core.Settings;
import com.megacrit.cardcrawl.localization.AchievementStrings;
import com.megacrit.cardcrawl.localization.BlightStrings;
import com.megacrit.cardcrawl.localization.CardStrings;
import com.megacrit.cardcrawl.localization.CharacterStrings;
import com.megacrit.cardcrawl.localization.CreditStrings;
import com.megacrit.cardcrawl.localization.EventStrings;
import com.megacrit.cardcrawl.localization.KeywordStrings;
import com.megacrit.cardcrawl.localization.MonsterStrings;
import com.megacrit.cardcrawl.localization.OrbStrings;
import com.megacrit.cardcrawl.localization.PotionStrings;
import com.megacrit.cardcrawl.localization.PowerStrings;
import com.megacrit.cardcrawl.localization.RelicStrings;
import com.megacrit.cardcrawl.localization.RunModStrings;
import com.megacrit.cardcrawl.localization.ScoreBonusStrings;
import com.megacrit.cardcrawl.localization.StanceStrings;
import com.megacrit.cardcrawl.localization.TutorialStrings;
import com.megacrit.cardcrawl.localization.UIStrings;

import basemod.BaseMod;
import basemod.interfaces.EditStringsSubscriber;
import basemod.interfaces.PostInitializeSubscriber;
import com.megacrit.cardcrawl.core.CardCrawlGame;
import com.megacrit.cardcrawl.cards.AbstractCard;
import com.megacrit.cardcrawl.helpers.CardLibrary;
import com.megacrit.cardcrawl.helpers.RelicLibrary;
import com.megacrit.cardcrawl.relics.AbstractRelic;

@SpireInitializer
public class SilksongLanguageMod implements EditStringsSubscriber, PostInitializeSubscriber {
    public static final Logger logger = LogManager.getLogger(SilksongLanguageMod.class.getName());
    
    // Mod信息
    public static final String MOD_ID = "com.silksong.lang";
    public static final String MOD_NAME = "Silksong Language Pack";
    public static final String VERSION = "1.0.0";
    
    // 语言设置
    public static final Settings.GameLanguage SILKSONG_ZH = Settings.GameLanguage.ZHS; // 使用简体中文作为基础
    public static final String LANGUAGE_STRINGS_PATH = "localization/silksong/";
    
    public SilksongLanguageMod() {
        logger.info("Initializing Silksong Language Mod");
        BaseMod.subscribe(this);
    }
    
    public static void initialize() {
        new SilksongLanguageMod();
    }
    
    @Override
    public void receiveEditStrings() {
        logger.info("Loading Silksong Language Pack...");
        
        try {
            // 根据当前语言设置加载相应的本地化文件
            loadLocalizations();
            logger.info("Silksong Language Pack loaded successfully!");
        } catch (Exception e) {
            logger.error("Failed to load Silksong Language Pack: ", e);
        }
    }
    
    // 在游戏完成初始化（进入主菜单）后，刷新已经加载的文本（卡牌、遗物等）
    @Override
    public void receivePostInitialize() {
        try {
            refreshRuntimeTexts();
        } catch (Exception e) {
            logger.error("Failed to refresh runtime texts: ", e);
        }
    }
    
    private void loadLocalizations() {
        // 无条件加载丝之歌体本地化文件，让BaseMod处理语言切换
        logger.info("Loading Silksong localization files...");
        
        // 加载卡牌本地化
        BaseMod.loadCustomStringsFile(CardStrings.class, 
            LANGUAGE_STRINGS_PATH + "cards.json");
        
        // 加载UI本地化
        BaseMod.loadCustomStringsFile(UIStrings.class, 
            LANGUAGE_STRINGS_PATH + "ui.json");
        
        // 加载角色本地化
        BaseMod.loadCustomStringsFile(CharacterStrings.class, 
            LANGUAGE_STRINGS_PATH + "characters.json");
        
        // 加载遗物本地化
        BaseMod.loadCustomStringsFile(RelicStrings.class, 
            LANGUAGE_STRINGS_PATH + "relics.json");
        
        // 加载怪物本地化
        BaseMod.loadCustomStringsFile(MonsterStrings.class, 
            LANGUAGE_STRINGS_PATH + "monsters.json");
        
        // 加载事件本地化
        BaseMod.loadCustomStringsFile(EventStrings.class, 
            LANGUAGE_STRINGS_PATH + "events.json");
        
        // 加载药水本地化
        BaseMod.loadCustomStringsFile(PotionStrings.class, 
            LANGUAGE_STRINGS_PATH + "potions.json");
        
        // 加载能力本地化
        BaseMod.loadCustomStringsFile(PowerStrings.class, 
            LANGUAGE_STRINGS_PATH + "powers.json");
        
        // 加载关键词本地化
        BaseMod.loadCustomStringsFile(KeywordStrings.class, 
            LANGUAGE_STRINGS_PATH + "keywords.json");
        
        // 加载球体本地化
        BaseMod.loadCustomStringsFile(OrbStrings.class, 
            LANGUAGE_STRINGS_PATH + "orbs.json");
        
        // 加载姿态本地化
        BaseMod.loadCustomStringsFile(StanceStrings.class, 
            LANGUAGE_STRINGS_PATH + "stances.json");
        
        // 加载教程本地化
        BaseMod.loadCustomStringsFile(TutorialStrings.class, 
            LANGUAGE_STRINGS_PATH + "tutorials.json");
        
        // 加载成就本地化
        BaseMod.loadCustomStringsFile(AchievementStrings.class, 
            LANGUAGE_STRINGS_PATH + "achievements.json");
        
        // 加载荒疫本地化
        BaseMod.loadCustomStringsFile(BlightStrings.class, 
            LANGUAGE_STRINGS_PATH + "blights.json");
        
        // 加载积分奖励本地化
        BaseMod.loadCustomStringsFile(ScoreBonusStrings.class, 
            LANGUAGE_STRINGS_PATH + "score_bonuses.json");
        
        // 加载运行模式本地化
        BaseMod.loadCustomStringsFile(RunModStrings.class, 
            LANGUAGE_STRINGS_PATH + "run_mods.json");
        
        // 加载制作人员本地化
        BaseMod.loadCustomStringsFile(CreditStrings.class, 
            LANGUAGE_STRINGS_PATH + "credits.json");
        
        logger.info("All Silksong localization files loaded successfully");
    }

    // 刷新当前已创建的对象（卡牌、遗物）的显示文本
    private void refreshRuntimeTexts() {
        logger.info("Refreshing runtime texts for cards and relics...");
        // 刷新卡牌
        try {
            java.util.List<AbstractCard> allCards = new java.util.ArrayList<>();
            try {
                Class<?> cl = Class.forName("com.megacrit.cardcrawl.helpers.CardLibrary");
                try {
                    java.lang.reflect.Method m = cl.getMethod("getAllCards");
                    Object res = m.invoke(null);
                    if (res instanceof java.util.Collection) {
                        for (Object o : (java.util.Collection<?>) res) {
                            if (o instanceof AbstractCard) {
                                allCards.add((AbstractCard) o);
                            }
                        }
                    }
                } catch (NoSuchMethodException nsme) {
                    java.lang.reflect.Field f = cl.getDeclaredField("cards");
                    f.setAccessible(true);
                    Object mapObj = f.get(null);
                    if (mapObj instanceof java.util.Map) {
                        for (Object o : ((java.util.Map<?, ?>) mapObj).values()) {
                            if (o instanceof AbstractCard) {
                                allCards.add((AbstractCard) o);
                            }
                        }
                    }
                }
            } catch (Throwable t) {
                logger.warn("Fallback to reflection for CardLibrary failed", t);
            }

            for (AbstractCard card : allCards) {
                CardStrings cs = CardCrawlGame.languagePack.getCardStrings(card.cardID);
                if (cs != null) {
                    card.name = cs.NAME;
                    card.rawDescription = cs.DESCRIPTION;
                    // 更新标题和描述（通过反射绕过protected）
                    try {
                        java.lang.reflect.Method mTitle = com.megacrit.cardcrawl.cards.AbstractCard.class.getDeclaredMethod("initializeTitle");
                        mTitle.setAccessible(true);
                        mTitle.invoke(card);
                    } catch (Throwable ignored) {}
                    try {
                        java.lang.reflect.Method mDesc = com.megacrit.cardcrawl.cards.AbstractCard.class.getDeclaredMethod("initializeDescription");
                        mDesc.setAccessible(true);
                        mDesc.invoke(card);
                    } catch (Throwable ignored) {}
                }
            }
            logger.info("Card texts refreshed");
        } catch (Throwable t) {
            logger.error("Failed to refresh card texts", t);
        }

        // 刷新遗物
        try {
            // 收集所有遗物实例（通过反射兼容不同版本的RelicLibrary结构）
            java.util.List<AbstractRelic> allRelics = new java.util.ArrayList<>();
            try {
                Class<?> rl = Class.forName("com.megacrit.cardcrawl.helpers.RelicLibrary");
                for (java.lang.reflect.Field f : rl.getDeclaredFields()) {
                    f.setAccessible(true);
                    if ((f.getModifiers() & java.lang.reflect.Modifier.STATIC) == 0) continue;
                    Object v = f.get(null);
                    if (v == null) continue;
                    if (v instanceof java.util.Map) {
                        for (Object o : ((java.util.Map<?, ?>) v).values()) {
                            if (o instanceof AbstractRelic) allRelics.add((AbstractRelic) o);
                        }
                    } else if (v instanceof java.util.Collection) {
                        for (Object o : (java.util.Collection<?>) v) {
                            if (o instanceof AbstractRelic) allRelics.add((AbstractRelic) o);
                        }
                    } else if (v.getClass().isArray()) {
                        int len = java.lang.reflect.Array.getLength(v);
                        for (int i = 0; i < len; i++) {
                            Object o = java.lang.reflect.Array.get(v, i);
                            if (o instanceof AbstractRelic) allRelics.add((AbstractRelic) o);
                        }
                    } else if (v instanceof AbstractRelic) {
                        allRelics.add((AbstractRelic) v);
                    }
                }
            } catch (Throwable ignore) {}

            for (AbstractRelic relic : allRelics) {
                RelicStrings rs = CardCrawlGame.languagePack.getRelicStrings(relic.relicId);
                if (rs != null) {
                    // 设置名称（通过反射处理可能的final字段）
                    try {
                        java.lang.reflect.Field fn = com.megacrit.cardcrawl.relics.AbstractRelic.class.getDeclaredField("name");
                        fn.setAccessible(true);
                        try {
                            java.lang.reflect.Field modField = java.lang.reflect.Field.class.getDeclaredField("modifiers");
                            modField.setAccessible(true);
                            modField.setInt(fn, fn.getModifiers() & ~java.lang.reflect.Modifier.FINAL);
                        } catch (Throwable ignored) {}
                        fn.set(relic, rs.NAME);
                    } catch (Throwable ignored) {}

                    // 计算描述
                    String newDesc = null;
                    try {
                        java.lang.reflect.Method m = com.megacrit.cardcrawl.relics.AbstractRelic.class.getDeclaredMethod("getUpdatedDescription");
                        m.setAccessible(true);
                        Object ret = m.invoke(relic);
                        if (ret instanceof String) newDesc = (String) ret;
                    } catch (Throwable ignored) {}
                    if (newDesc == null) {
                        if (rs.DESCRIPTIONS != null && rs.DESCRIPTIONS.length > 0) {
                            StringBuilder sb = new StringBuilder();
                            for (String s : rs.DESCRIPTIONS) sb.append(s);
                            newDesc = sb.toString();
                        }
                    }
                    if (newDesc != null) {
                        try {
                            java.lang.reflect.Field fd = com.megacrit.cardcrawl.relics.AbstractRelic.class.getDeclaredField("description");
                            fd.setAccessible(true);
                            try {
                                java.lang.reflect.Field modField2 = java.lang.reflect.Field.class.getDeclaredField("modifiers");
                                modField2.setAccessible(true);
                                modField2.setInt(fd, fd.getModifiers() & ~java.lang.reflect.Modifier.FINAL);
                            } catch (Throwable ignored) {}
                            fd.set(relic, newDesc);
                        } catch (Throwable ignored) {}
                    }

                    // 重新初始化提示（通过反射绕过protected）
                    try {
                        java.lang.reflect.Method mTips = com.megacrit.cardcrawl.relics.AbstractRelic.class.getDeclaredMethod("initializeTips");
                        mTips.setAccessible(true);
                        mTips.invoke(relic);
                    } catch (Throwable ignored) {}
                }
            }
            logger.info("Relic texts refreshed");
        } catch (Throwable t) {
            logger.error("Failed to refresh relic texts", t);
        }
    }
}