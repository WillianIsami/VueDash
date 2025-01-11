<template>
  <div class="book-card">
    <img :src="book.image_medium" :alt="book.title" class="book-cover" />
    <h3>{{ book.title }}</h3>
    <p>By: {{ book.author }}</p>
    <p>Published: {{ book.year }}</p>
  </div>
</template>

<script setup lang="ts">
interface Book {
  isbn: string;
  title: string;
  author: string;
  year: number;
  imageUrlM: string;
}

defineProps<{
  book: Book;
}>();
</script>

<style scoped>
.book-card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin: 1rem;
  max-width: 300px;
}

.book-cover {
  max-width: 100%;
  height: auto;
}
</style>
