<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Popular Books</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="book in books" :key="book.isbn">
        <BookCard :book="book" />
      </div>
    </div>

    <!-- Loader to infinite scroll -->
    <div v-if="hasMore" ref="loader" class="text-center py-4">
      <div v-if="isLoading">
        Loading...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import BookCard from '@/components/BookCard.vue';

const books = ref([]);
const offset = ref(0);
const limit = 10;
const hasMore = ref(true);
const loader = ref(null);
const isLoading = ref(false);

// Function to load books
const loadBooks = async () => { 
  isLoading.value = true;

  try {
    const baseUrl = 'http://localhost:8000/api/v1/books/popular';
    const newBooks = await $fetch(baseUrl, {
      params: {
        limit,
        offset: offset.value,
      },
    });
    if (newBooks.length) {
      books.value.push(...newBooks);
      offset.value += limit;
    } else {
      hasMore.value = false;
    }
  } catch (err) {
    console.error('Error loading items:', err);
    error.value = 'Error loading books. Please try again.';
  } finally {
    isLoading.value = false; 
  }
};

// Setup Intersection Observer
onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      const [entry] = entries;
      if (entry.isIntersecting && hasMore.value) {
        loadBooks();
      }
    },
    {
      rootMargin: '20px',
    }
  );

  if (loader.value) {
    observer.observe(loader.value);
  }

  // Cleanup
  onBeforeUnmount(() => {
    if (loader.value) {
      observer.unobserve(loader.value);
    }
  });
});
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