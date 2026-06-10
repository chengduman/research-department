# PR 模板（适配所有部门）
name: 📦 交付物提交
description: 提交工作交付物供部长审核
title: "[提交] "
labels: ["待审核"]
body:
  - type: markdown
    attributes:
      value: |
        ## 交付物提交
        提交人：________    日期：________
  - type: input
    id: task-ref
    attributes:
      label: 关联 Issue/Task
      description: 关联的任务或需求 Issue 编号
      placeholder: #123
    validations:
      required: true
  - type: textarea
    id: deliverables
    attributes:
      label: 交付物清单
      placeholder: 列出交付的文件/代码/设计稿等
    validations:
      required: true
  - type: textarea
    id: summary
    attributes:
      label: 内容概要
      placeholder: 简述交付物的核心内容和亮点
    validations:
      required: true
  - type: checkboxes
    id: self-check
    attributes:
      label: 自检清单
      options:
        - label: 已通过自检，质量达标
        - label: 已按规范命名和归档
        - label: 必要时已附数据来源
  - type: textarea
    id: notes
    attributes:
      label: 需要部长关注的要点
      placeholder: 如有特殊情况或需要讨论的问题
