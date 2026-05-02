/**
 * FAQ 智能检索脚本
 * 功能：用户问题 → 匹配最相关的FAQ → 返回答案
 *
 * 使用方式：
 *   node faq_retrieval.js "你们最大能做多大的桶"
 *
 * 输出格式：
 *   {
 *     "matched": true,
 *     "question": "你们最大能做多大的桶？",
 *     "answer": "我们的储料式机型覆盖30L到200L容量范围...",
 *     "category": "产品选型",
 *     "confidence": 0.95
 *   }
 */

const fs = require('fs');
const path = require('path');

// 加载FAQ知识库
function loadKnowledgeBase() {
  const kbPath = path.join(__dirname, 'faq_knowledge_base.json');
  const data = fs.readFileSync(kbPath, 'utf8');
  return JSON.parse(data);
}

// 计算两个字符串的相似度（简单词匹配）
function calculateSimilarity(query, text) {
  const queryWords = query.toLowerCase().replace(/[？，。！？、]/g, '').split(/\s+/);
  const textLower = text.toLowerCase().replace(/[？，。！？、]/g, '');

  let matchCount = 0;
  for (const word of queryWords) {
    if (textLower.includes(word) && word.length >= 2) {
      matchCount++;
    }
  }

  if (queryWords.length === 0) return 0;
  return matchCount / queryWords.length;
}

// 检索最匹配的FAQ
function findBestMatch(query, knowledgeBase) {
  let bestMatch = null;
  let bestScore = 0;

  for (const faq of knowledgeBase.faq_data) {
    // 计算与问题的相似度
    const questionScore = calculateSimilarity(query, faq.question);

    // 计算与答案的相似度
    const answerScore = calculateSimilarity(query, faq.answer) * 0.3;

    // 计算综合得分
    const totalScore = questionScore + answerScore;

    // 也考虑标签匹配
    let tagScore = 0;
    for (const tag of faq.tags || []) {
      if (query.includes(tag)) {
        tagScore += 0.2;
      }
    }

    const finalScore = totalScore + tagScore;

    if (finalScore > bestScore) {
      bestScore = finalScore;
      bestMatch = faq;
    }
  }

  return {
    match: bestMatch,
    score: bestScore
  };
}

// 处理用户查询
function processQuery(query) {
  const knowledgeBase = loadKnowledgeBase();
  const { match, score } = findBestMatch(query, knowledgeBase);

  if (!match || score < 0.1) {
    return {
      matched: false,
      message: '抱歉，我没有找到相关的答案。请联系销售获取帮助：138-2968-XXXX',
      category: null,
      confidence: 0
    };
  }

  return {
    matched: true,
    question: match.question,
    answer: match.answer,
    category: match.category,
    source: match.source,
    tags: match.tags,
    confidence: Math.min(score, 1),
    suggestions: getSuggestions(match.category, knowledgeBase)
  };
}

// 获取同类目下的其他问题作为建议
function getSuggestions(category, knowledgeBase) {
  const sameCategory = knowledgeBase.faq_data
    .filter(faq => faq.category === category)
    .slice(0, 3)
    .map(faq => faq.question);
  return sameCategory;
}

// 命令行入口
if (require.main === module) {
  const query = process.argv[2];

  if (!query) {
    console.log('用法: node faq_retrieval.js "您的问题"');
    process.exit(1);
  }

  const result = processQuery(query);
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { processQuery, loadKnowledgeBase };
