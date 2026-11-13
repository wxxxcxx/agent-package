## 它做什么

`grilling` 是一套访谈回路，用来在任何人动手之前压力测试一个计划、一个决策或一个想法。它把讨论对象画成 **design tree**（设计树）：每个决策都分叉出依附于它的决策；它按分支一路问下去，直到没有任何假设还留在暗处。

它不问一题答一题，也不一次问光。每一 **round** 问一个完整的 **frontier**：所有前置条件已经落定的决策，别的都不问。两个问题只要互相依赖，就不进同一 round；依赖尚未答复的问题，属于后面的 round。你的回答让决策落定，frontier 随之向外推，下一 round 就问刚被解开的部分。十三个问题通常落在三个 round 左右，而不是十三轮。

## 什么时候用它

输入 `/grilling`，或者任务合适时由 agent 自己取用。grilling 家族里只有它是 model-invoked，所以你很少手打。通常是你在用的某个 skill 替你调起它。

直接输入 `/grilling`，得到的是一场单纯的访谈，没有别的。需要更多时：

| 你手上的情况 | 该用 |
| --- | --- |
| 不在工作目录里 | grill-me：同一次 session，名字 agent 永远不会自己触发 |
| 在工作目录里 | grill-with-docs：同一次 session，边问边写 `GLOSSARY.md` 和 ADR |
| 一件事大到一次 session 装不下 | wayfinder：画一张地图，在决策 ticket 里跑 grilling |
| 谈话解决不了的问题：某个东西该长什么样、什么手感 | prototype：先做丢弃版，再回来 |
| 自己的 skill 需要一场访谈 | 在里面调 `/grilling`，不要另写一套 |

## round、frontier，以及谁做决定

这个 skill 立在三个概念上。

**design tree** 是讨论对象的模型：决策之上挂着决策。**frontier** 是前置条件全部落定的那批决策：agent 此刻唯一能问的问题。**round** 是一个 frontier，问全，也答全。

一个 round 之内，每个问题格式固定：编号、加标题，前置 `❓`，然后是正文，最后单独一行 `➡️` 放 agent 推荐的回答。这个格式让你按编号答完整轮（「1 是，2 选第二个，3 不，因为…」），不必把问题复制回来。格式有一个已知问题：推荐有时在反驳问题本身的措辞，此时同意推荐等于对问题答「不」。遇到这种情况，直接答推荐，并说明。

设计的另一半，是事实与决策的分工。事实是 skill 自己的活。frontier 上的问题需要环境（文件系统、工具）才能确定时，agent 派一个 subagent 去查，不要问你。round 不等这项探查；只有依赖它的那些问题等。决策是你的，agent 必须等。跑 `grilling` 的 agent 自己替你把决策答了，就是把这个 skill 弄坏了。frontier 空了，session 结束；此后 agent 还要等你确认双方理解一致，才动手。

frontier 有一个限度：它靠判断选出，不是从图上算出来的。所以它可能把两个问题放进一个 round，过一阵才发现其中一个答案本该改动另一个。唯一的护栏是你说出来；下一 round 重开受影响的那条分支。

## 哪些内容在这里，哪些在外层

本页讲机制。外层 skill 的页面回答大家问得最多的那些问题。

| 问题 | 答案在哪 |
| --- | --- |
| design tree、frontier、round、问题格式、事实与决策 | 这里 |
| 一次 session 该跑多久、谈不出答案的问题怎么办、怎么避免一路点头 | grill-me |
| `GLOSSARY.md` 写什么、什么该成为 ADR | grill-with-docs |

## 常见问题

**能不能改回一次问一题？**

可以，而且相当一部分人就这么用。在你的全局 `CLAUDE.md` 里加一行：

```
When grilling, ask one question at a time.
```

并非所有人都喜欢按 round 的默认做法。读得慢的人、用第二语言工作的人、靠逐题推进来集中注意力的人，都反馈一次一题更好用。这条退路是受支持的设置，不是权宜之计。

**`/batch-grill-me` 去哪了？**

并进了这个 skill。按 round 提问曾短暂作为独立 skill 发布，后来移进 `grilling`，于是建在它上面的一切（grill-me、grill-with-docs、triage、wayfinder）同时拿到了它。没有 `batch-grill-me` 可装，也没有另立的逐题 skill；上面那行 `CLAUDE.md` 就是回到一次一题的路。

**一轮问这么多，岂不是丢掉了我前面回答才会引出的问题？**

这是对 round 最常见的反对，frontier 正好回答它。一个 round 里只放互不依赖的问题，所以本轮任何一个回答都不会让同轮另一个问题失效。你的回答仍然改变后面：下一 round 是 agent 从零重算的。确实会丢一点，但比「一次问光」听起来少得多。参见上面 frontier 的限度。

**问题问完了，它直接开始干活了。**

确认闸门就是为此设的。这个 skill 结束于你说理解一致，不是 frontier 空了。能力弱、速度快的 model 仍会跳过闸门。用户报告多见于低 reasoning 或非前沿 model，它们把「访谈直到理解一致」压成几个问题加一份提纲。你的模型这样，可靠的修法是在自己的 `AGENTS.md` 或 `CLAUDE.md` 写一行：未经许可不得实施。

**它自问自答，不问我。**

那是这一轮跑坏了，也正是 skill 正文要分开事实与决策的原因。最常见于另一个 skill 调 `grilling` 去结一个 ticket，agent 把那个任务当成了继续推进的许可。同一条约束也是没有 async 模式的原因。有人要过一种变体：读一个 GitHub issue，发一份汇总的决策备忘。那是另一个 skill，因为没人回答的 grilling，产出的只是 agent 的意见，不是你的。

**能不能限制问题数量？**

不能，上限是故意不做的。有的计划三个问题够，有的要五十个；固定上限要么截断难的那件，要么在容易的那件上显得随意。预设的控制手段是自然语言：让它收尾，或者停在当前计划上接受它。session 跑得特别长，通常是范围太大；把活拆小，分别 grill。

**我单独装了 grill-me，没反应。**

grill-me 是一行 skill，正文就是「跑一次 `/grilling` session」，所以它需要 grilling 也装好。grill-with-docs 同理，另外还要 domain-modeling。整套装上就没这问题；挑着装，就得把底层的也装上。

**grill-with-docs 跑了，但没加载 grilling。**

这是真 bug，至今未修，跨 harness、跨 model 都有人报。一个 skill 点名另一个 skill，不保证后者被加载，而 grill-with-docs 点了两个。症状是一场把所有问题一次抛出来、也没有推荐的 session：那说明模型在即兴访谈，而不是在跑这一套。直接问 agent 有没有加载 grilling 和 domain-modeling，通常能救回来。

## 它在正常工作时

- 一个 round 以编号列表到达，每题一句 `➡️` 推荐，你可以按编号答完整轮。
- 一轮里没有任何问题需要先等同轮另一题。
- 后面的 round 问到第一轮问不出来的东西。
- 它自己去查事实（读文件、派 subagent），而不是问你本可查到的事。
- 后台探查不拖住 round；只有依赖它的那几题等。
- 结束时它停下来，请你确认理解一致，而不是开工。
- 问题数一直高，round 数一直低。

## 它的位置

grilling 是**原语**，不是排进流程的一步：访谈技法只有一个真相源，集中在一处，让所有需要访谈的 skill 取用它，而不是各写一套。grill-me 与 grill-with-docs 是它两个面向用户的正门，主构建链从 grill-with-docs 开始，排在 to-spec 之前。wayfinder 用它解决策 ticket，triage 用它把含糊的报告 grill 成能做的报告，improve-codebase-architecture 在你选定了要 deepening 的候选之后用它走完这棵树。不确定该走哪个入口时，由 ask-matt 分流。
