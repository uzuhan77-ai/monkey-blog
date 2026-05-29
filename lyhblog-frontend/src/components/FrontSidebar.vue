<template>
  <aside class="sidebar">
    <div class="card">
      <div class="avatar">LYH</div>
      <h1>LYH BLOG</h1>
      <p>记录AI编程和项目实践</p>
    </div>

    <div class="card">
      <h3>分类</h3>
      <button
      v-for="category in categoryList" 
      :key="category.id"
      :class="{active: categoryId == category.id}"
      @click="$emit('select-category', category.id)"
      >
        {{ category.name }}
      </button>
    </div>


    <div class="card">
      <h3>标签</h3>
      <button 
        v-for="tag in tagList"
        :key="tag.id"
        :class="{active: tagId == tag.id}"
        @click="$emit('select-tag', tag.id)"
      >
        {{ tag.name }}
      </button>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  categoryList: { type: Array, default: () => [] },
  tagList: {type: Array, default: () => []},
  categoryId: {type: [Number, String, null], default: null},
  tagId: {type: [Number, String, null], default: null},
})

defineEmits(['select-category', 'select-tag'])
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-self: start;
  position: sticky;
  top: 94px;
}

.card {
  border: 1px solid rgba(31, 36, 48, 0.06);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
  backdrop-filter: blur(16px);
  overflow: hidden;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.card:hover {
  border-color: rgba(47, 141, 244, 0.11);
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

.card:first-child {
  padding: 12px 12px 18px;
  text-align: center;
}

.avatar {
  width: 100%;
  aspect-ratio: 1 / 0.76;
  margin: 0 auto 16px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background:
    linear-gradient(135deg, rgba(47, 141, 244, 0.18), rgba(255, 255, 255, 0.58)),
    rgba(47, 141, 244, 0.085);
  color: #2f8df4;
  font-size: 29px;
  font-weight: 800;
  box-shadow:
    inset 0 0 0 1px rgba(47, 141, 244, 0.1),
    0 8px 20px rgba(47, 141, 244, 0.075);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.card:first-child:hover .avatar {
  transform: translateY(-1px);
  box-shadow:
    inset 0 0 0 1px rgba(47, 141, 244, 0.14),
    0 12px 28px rgba(47, 141, 244, 0.11);
}

.card h1,
.card h2 {
  margin: 0;
  color: rgba(31, 36, 48, 0.92);
  font-size: 22px;
  line-height: 1.16;
  letter-spacing: 0;
}

.card h1::after {
  content: "";
  display: block;
  width: 24px;
  height: 4px;
  margin: 12px auto 0;
  border-radius: 999px;
  background: #2f8df4;
}

.card p {
  margin: 9px 4px 0;
  color: rgba(31, 36, 48, 0.52);
  font-size: 14px;
  line-height: 1.65;
}

.card:not(:first-child) {
  padding: 16px 16px 14px;
}

.card h3 {
  position: relative;
  margin: 0 0 14px;
  padding-left: 14px;
  color: rgba(31, 36, 48, 0.9);
  font-size: 17px;
  line-height: 1.3;
}

.card h3::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.18em;
  width: 4px;
  height: 1.08em;
  border-radius: 999px;
  background: #2f8df4;
}

.card button {
  min-height: 36px;
  border: 0;
  border-radius: 11px;
  background: transparent;
  color: rgba(31, 36, 48, 0.68);
  font-size: 13px;
  font-weight: 650;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    padding 0.2s ease,
    background 0.2s ease,
    color 0.2s ease,
    box-shadow 0.2s ease;
}

.card:nth-child(2) button {
  width: 100%;
  margin: 0 0 6px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: left;
  background: rgba(31, 36, 48, 0.025);
}

.card:nth-child(2) button:last-child {
  margin-bottom: 0;
}

.card:nth-child(3) button {
  min-height: 32px;
  margin: 0 7px 8px 0;
  padding: 5px 11px;
  background: rgba(47, 141, 244, 0.07);
  color: rgba(47, 111, 171, 0.88);
}

.card button:hover,
.card button.active {
  background: rgba(47, 141, 244, 0.105);
  color: #2f8df4;
}

.card:nth-child(2) button:hover,
.card:nth-child(2) button.active {
  padding-left: 15px;
  transform: translateX(1px);
  box-shadow: inset 3px 0 0 rgba(47, 141, 244, 0.7);
}

.card:nth-child(3) button:hover,
.card:nth-child(3) button.active {
  background: rgba(47, 141, 244, 0.14);
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(47, 141, 244, 0.08);
}

.card button:focus-visible {
  outline: 2px solid rgba(47, 141, 244, 0.35);
  outline-offset: 2px;
}

@media (max-width: 900px) {
  .sidebar {
    position: static;
  }

  .card:first-child {
    text-align: left;
  }

  .avatar {
    width: 116px;
    height: 116px;
    aspect-ratio: auto;
    margin-left: 0;
  }

  .card h1::after {
    margin-left: 0;
  }
}
</style>
