# Silksong Language Pack - 丝之歌体语言包

《杀戮尖塔》丝之歌体本地化mod，提供古典文言文风格的中文本地化体验。

## 功能特色

- 🎨 **古典文言文风格** - 独特的古风文本体验
- 📚 **完整本地化** - 覆盖游戏所有内容（卡牌、UI、角色、遗物等）
- 🔄 **即时切换** - 通过游戏内语言设置即可切换
- ⚖️ **平衡保持** - 不影响游戏平衡性

## 安装方法

### 方法一：直接安装（推荐）
1. 下载编译好的 `silksong-language.jar` 文件
2. 将jar文件放入 `SlayTheSpire/mods/` 目录
3. 启动游戏，在设置中将语言切换为对应选项

### 方法二：从源码构建

#### 前置要求
- Java 8 或更高版本
- Maven 3.6+
- 《杀戮尖塔》游戏本体
- ModTheSpire
- BaseMod

#### 构建步骤

1. **准备依赖文件**
   
   将以下文件复制到 `lib/` 目录：
   ```
   lib/
   ├── desktop-1.0.jar      # 从游戏安装目录复制
   ├── ModTheSpire.jar      # 从ModTheSpire安装目录复制
   └── BaseMod.jar          # 从BaseMod下载页面获取
   ```

2. **编译项目**
   ```bash
   mvn clean compile
   ```

3. **打包mod**
   ```bash
   mvn package
   ```

4. **安装mod**
   
   将生成的 `target/silksong-language.jar` 复制到游戏的mods目录

## 项目结构

```
sts-mod-silksong-language/
├── src/main/java/com/silksong/lang/
│   └── SilksongLanguageMod.java          # 主mod类
├── src/main/resources/localization/silksong/
│   ├── cards.json                        # 卡牌本地化
│   ├── ui.json                          # UI本地化
│   ├── characters.json                  # 角色本地化
│   ├── relics.json                      # 遗物本地化
│   ├── monsters.json                    # 怪物本地化
│   ├── events.json                      # 事件本地化
│   ├── potions.json                     # 药水本地化
│   ├── powers.json                      # 能力本地化
│   ├── keywords.json                    # 关键词本地化
│   ├── orbs.json                        # 球体本地化
│   ├── stances.json                     # 姿态本地化
│   ├── tutorials.json                   # 教程本地化
│   ├── achievements.json                # 成就本地化
│   ├── blights.json                     # 荒疫本地化
│   ├── score_bonuses.json               # 积分奖励本地化
│   ├── run_mods.json                    # 运行模式本地化
│   └── credits.json                     # 制作人员本地化
├── lib/                                 # 依赖jar文件目录
├── pom.xml                              # Maven配置
├── ModTheSpire.json                     # Mod元数据
└── README.md                            # 项目说明
```

## 使用说明

1. 确保已安装ModTheSpire和BaseMod
2. 将mod文件放入mods目录
3. 启动游戏
4. 在游戏设置中切换语言即可体验丝之歌体本地化

## 技术说明

- **Mod ID**: `com.silksong.lang`
- **依赖**: BaseMod 5.15.0+
- **兼容性**: 支持《杀戮尖塔》12-22-2020版本
- **语言代码**: 基于简体中文(ZHS)扩展

## 贡献

欢迎提交问题报告和改进建议！

## 许可证

本项目遵循开源许可证，详情请查看LICENSE文件。

---

*愿君于尖塔之巅，得见丝歌之美。*