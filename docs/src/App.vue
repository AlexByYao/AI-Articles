<template>
  <div class="app">
    <div class="header">
      <div class="brand">
        <div class="logo"></div>
        <div class="title">
          <h1>C++ / Qt 面试题库</h1>
          <p>每日更新 · 搜索 · 难度筛选 · 低重复度</p>
        </div>
      </div>

      <div class="toolbar">
        <input class="input" v-model="keyword" placeholder="搜索题目/关键词" />
        <select class="select" v-model="difficulty">
          <option value="all">全部难度</option>
          <option value="easy">简单</option>
          <option value="medium">稍难</option>
          <option value="hard">较难</option>
        </select>
      </div>
    </div>

    <div class="stats">
      <div>共 {{ filteredCount }} 题</div>
      <div>数据日期：{{ dataDates.join(" / ") || "暂无" }}</div>
    </div>

    <div v-for="(group, date) in grouped" :key="date" class="group">
      <h2>📅 {{ date }}</h2>
      <div class="cards">
        <div v-for="q in group" :key="q.id" class="card">
          <h3>{{ q.question }}</h3>
          <div class="meta">
            <span class="chip">{{ mapDifficulty(q.difficulty) }}</span>
            <span class="chip">{{ q.topic }}</span>
          </div>

          <div v-if="q.showAnswer" class="answer">
            {{ q.answer }}
          </div>
          <div class="toggle" @click="q.showAnswer = !q.showAnswer">
            <span>{{ q.showAnswer ? "收起答案" : "展开答案" }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">© AI-Articles · 自动更新</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const all = ref([])
const keyword = ref('')
const difficulty = ref('all')

const dataDates = ref([])

const mapDifficulty = (d) => {
  if (d === 'easy') return '简单'
  if (d === 'medium') return '稍难'
  if (d === 'hard') return '较难'
  return d
}

const filtered = computed(() => {
  return all.value.filter(q => {
    const okDiff = difficulty.value === 'all' || q.difficulty === difficulty.value
    const kw = keyword.value.trim().toLowerCase()
    const okKw = !kw || q.question.toLowerCase().includes(kw) || q.answer.toLowerCase().includes(kw)
    return okDiff && okKw
  })
})

const filteredCount = computed(() => filtered.value.length)

const grouped = computed(() => {
  const map = {}
  for (const q of filtered.value) {
    const d = q.date || '未知日期'
    if (!map[d]) map[d] = []
    map[d].push(q)
  }
  return map
})

onMounted(async () => {
  const res = await fetch(`${import.meta.env.BASE_URL}data/index.json`)
  const index = await res.json()
  dataDates.value = index.dates || []

  const allData = []
  for (const date of dataDates.value) {
    const r = await fetch(`${import.meta.env.BASE_URL}data/${date}.json`)
    const j = await r.json()
    for (const q of j.questions) {
      allData.push({ ...q, date, showAnswer: false })
    }
  }
  all.value = allData
})
</script>
