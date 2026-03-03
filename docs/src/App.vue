<template>
  <div class="app">
    <div class="header">
      <div class="brand">
        <div class="logo"></div>
        <div class="title">
          <h1>C++ / Qt 面试题库</h1>
          <p>每日更新 · 搜索 · 难度/日期筛选 · 列表直显答案</p>
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
        <select class="select" v-model="dateFilter">
          <option value="all">全部日期</option>
          <option v-for="d in dataDates" :key="d" :value="d">{{ d }}</option>
        </select>
        <select class="select" v-model="topicFilter">
          <option value="all">全部主题</option>
          <option v-for="t in topics" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>
    </div>

    <div class="stats">
      <div>共 {{ filteredCount }} 题</div>
      <div>数据日期：{{ dataDates.join(" / ") || "暂无" }}</div>
    </div>

    <div v-for="(group, date) in grouped" :key="date" class="group">
      <h2>📅 {{ date }}</h2>
      <div class="list">
        <div v-for="q in group" :key="q.id" class="item">
          <div class="item-head">
            <span class="qid">{{ q.id }}</span>
            <h3>{{ q.question }}</h3>
          </div>
          <div class="meta">
            <span class="chip">{{ mapDifficulty(q.difficulty) }}</span>
            <span class="chip">{{ q.topic }}</span>
          </div>
          <div class="answer">
            {{ q.answer }}
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
const dateFilter = ref('all')
const topicFilter = ref('all')

const dataDates = ref([])

const mapDifficulty = (d) => {
  if (d === 'easy') return '简单'
  if (d === 'medium') return '稍难'
  if (d === 'hard') return '较难'
  return d
}

const topics = computed(() => {
  const set = new Set(all.value.map(q => q.topic).filter(Boolean))
  return Array.from(set)
})

const filtered = computed(() => {
  return all.value.filter(q => {
    const okDiff = difficulty.value === 'all' || q.difficulty === difficulty.value
    const okDate = dateFilter.value === 'all' || q.date === dateFilter.value
    const okTopic = topicFilter.value === 'all' || q.topic === topicFilter.value
    const kw = keyword.value.trim().toLowerCase()
    const okKw = !kw || q.question.toLowerCase().includes(kw) || q.answer.toLowerCase().includes(kw)
    return okDiff && okDate && okTopic && okKw
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
      allData.push({ ...q, date })
    }
  }
  all.value = allData
})
</script>
