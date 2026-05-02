#!/usr/bin/env node
/**
 * faq_retrieve.js
 * FAQ检索工具 - Claude调用专用
 * 用法: node faq_retrieve.js "客户消息文本"
 * 
 * 返回: 最匹配的FAQ记录（JSON格式）
 */

const fs = require('fs');
const path = require('path');

// 加载FAQ知识库
const faqData = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, 'chat_knowledge_base_v2.json'),
    'utf8'
  )
);

// 加载意向识别规则
const intentRules = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, 'intent_detection_rules.json'),
    'utf8'
  )
);

/**
 * 检测客户消息的意图类型
 * @param {string} message - 客户消息
 * @returns {object} - { intent: string, action: string, matched_keywords: string[] }
 */
function detectIntent(message) {
  const lowerMessage = message.toLowerCase();
  const signals = intentRules;
  
  for (const [intentType, rule] of Object.entries(signals)) {
    const matches = rule.keywords.filter(kw => lowerMessage.includes(kw.toLowerCase()));
    if (matches.length >= rule.threshold) {
      return {
        intent: intentType,
        action: rule.action,
        matched_keywords: matches
      };
    }
  }
  
  return { intent: 'unknown', action: 'route_to_knowledge_base', matched_keywords: [] };
}

/**
 * 计算消息与FAQ的匹配分数
 * @param {string} message - 客户消息
 * @param {object} faq - FAQ记录
 * @returns {number} - 匹配分数
 */
function calculateScore(message, faq) {
  const lowerMessage = message.toLowerCase();
  let score = 0;
  
  // keywords匹配（最高权重）
  for (const kw of faq.keywords || []) {
    if (lowerMessage.includes(kw.toLowerCase())) {
      score += 10;
    }
  }
  
  // question_patterns匹配（高权重）
  for (const pattern of faq.question_patterns || []) {
    if (lowerMessage.includes(pattern.toLowerCase())) {
      score += 5;
    }
  }
  
  return score;
}

/**
 * 检索最匹配的FAQ
 * @param {string} message - 客户消息
 * @param {string} intentFilter - 可选：按intent过滤
 * @returns {object} - 匹配结果
 */
function faqRetrieve(message, intentFilter = null) {
  // 1. 先检测意图
  const intentResult = detectIntent(message);
  
  // 2. 如果有intent_filter，按filter过滤
  let candidates = faqData.faq_data;
  if (intentFilter) {
    candidates = candidates.filter(faq => 
      faq.intent && faq.intent.includes(intentFilter)
    );
  }
  
  // 3. 计算每个FAQ的匹配分数
  const scored = candidates.map(faq => ({
    faq,
    score: calculateScore(message, faq)
  }));
  
  // 4. 按分数排序，取最高分
  scored.sort((a, b) => b.score - a.score);
  
  const best = scored[0];
  
  if (!best || best.score === 0) {
    return {
      matched: false,
      intent: intentResult,
      faq: null,
      suggested_response: getSuggestedResponse(intentResult)
    };
  }
  
  return {
    matched: true,
    intent: intentResult,
    faq: {
      id: best.faq.id,
      category: best.faq.category,
      answer: best.faq.answer,
      response_type: best.faq.response_type,
      follow_up: best.faq.follow_up || null,
      leads_trigger: best.faq.leads_trigger || false,
      fault_related: best.faq.fault_related || false
    },
    confidence: best.score
  };
}

/**
 * 获取建议回复（当没有匹配到FAQ时）
 */
function getSuggestedResponse(intentResult) {
  const templates = faqData.quick_reply_templates;
  
  switch (intentResult.action) {
    case 'collect_leads':
      return templates.leads_prompt || "为了更好地为您服务，请留下您的联系方式。";
    case 'route_to_fault_report':
      return templates.fault_report_prompt;
    case 'show_greeting':
      return templates.greeting;
    default:
      return templates.unknown;
  }
}

// 命令行接口
if (require.main === module) {
  const message = process.argv.slice(2).join(' ');
  
  if (!message) {
    console.log('用法: node faq_retrieve.js "客户消息文本"');
    process.exit(1);
  }
  
  const result = faqRetrieve(message);
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { faqRetrieve, detectIntent };
