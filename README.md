# Silksong Language Pack - 丝之歌体语言包

> 本项目由Trae生成

《杀戮尖塔》丝之歌体本地化mod，提供古典文言文风格的中文本地化体验。

## 功能特色

你现在是「文盲古文小生」翻译师。将正常中文改写为《空洞骑士：丝之歌》的玄虚风格：

【翻译规则】
1. 核心技法：错置词性语序、乱用拟古词。无需强求改写，适时保留原文，只对有玄虚效果的部分进行修改。
2. 字数控制：与原文大体一致
3. 可读性：确保玩家只能模糊地理解基本含义，不知所云

## 安装方法

### 方法一：直接安装（推荐）
1. 下载编译好的 `silksong-language.jar` 文件
2. 将jar文件放入 `SlayTheSpire/mods/` 目录
3. 启动游戏，在设置中将语言切换为简体中文

### 方法二：从源码构建

#### 前置要求
- Java 8 或更高版本
- Maven 3.6+
- 《杀戮尖塔》游戏本体
- ModTheSpire
- BaseMod

#### 构建步骤

1. **修改maven里的Steam.path**
   
   安装了杀戮尖塔及mod的路径 

2. **编译项目**
   ```bash
   mvn clean compile
   ```

3. **打包mod**
   ```bash
   mvn package
   ```

4. **安装mod**
   
   生成的 `silksong-language.jar` 会自动复制到游戏的mods目录


## 手动翻译

1. 将杀戮尖塔本体desktop-1.0.jar解压，提取中文本地化目录zhs/*.json，放到本目录下
2. 配置Deepseek或者任何OpenAI模型的调用信息
```
export OPENAI_API_KEY=
export OPENAI_API_URL=
python trans.py zhs/cards.json
```

逐个文件调用，每次调用会翻译150条记录。详见代码，代码问题可以问AI

---

*愿君于尖塔之巅，得见丝歌之美。*