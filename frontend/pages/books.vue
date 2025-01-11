<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Books</h1>
    
    <!-- Search form -->
    <div class="mb-6 p-4 bg-gray-100 rounded">
      <div class="flex flex-col gap-4">
        <div class="flex gap-4">
          <select 
            v-model="searchType" 
            class="p-2 border rounded"
          >
            <option value="user">Search by User ID</option>
            <option value="isbn">Search by ISBN</option>
          </select>
          
          <input 
            v-model="searchValue" 
            :placeholder="searchType === 'user' ? 'Enter User ID' : 'Enter ISBN'"
            class="p-2 border rounded flex-grow"
            type="text"
          />
          
          <button 
            @click="handleSearch" 
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Search
          </button>
        </div>
        
        <div v-if="error" class="text-red-500">
          {{ error }}
        </div>
      </div>
    </div>

    <!-- No results message -->
    <div v-if="showNoResults" class="text-gray-500 text-center">
      <p v-if="searchType === 'user'">
        No recommendations found for this User ID. Try searching for popular books instead.
      </p>
      <p v-if="searchType === 'isbn'">
        No books found for the given ISBN. This book might not be available.
      </p>
    </div>

    <!-- Book list -->
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
const error = ref('');
const showNoResults = ref(false);
const isLoading = ref(false);

// New refs for search control
const searchType = ref('user');
const searchValue = ref('');

// Function to build the URL based on the search type
const getApiUrl = () => {
  const baseUrl = 'http://localhost:8000/api/v1/recommendations';
  if (searchType.value === 'user') {
    return `${baseUrl}/user/${searchValue.value}`;
  }
  return `${baseUrl}/similar/${searchValue.value}`;
};

// Function to reset the search state
const resetSearch = () => {
  books.value = [];
  offset.value = 0;
  hasMore.value = true;
  error.value = '';
};

// Function to load books
const loadBooks = async () => {
  if (!searchValue.value) return;
  
  isLoading.value = true;

  try {
    const url = getApiUrl();
    const newBooks = await $fetch(url, {
      params: {
        limit,
        offset: offset.value,
      },
    });
    if (offset.value === 0 && newBooks.length === 0) {
      showNoResults.value = true;
    } else {
      showNoResults.value = false;
    }

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

const handleSearch = () => {
  if (!searchValue.value) {
    error.value = 'Please enter a value to search for';
    return;
  }
  resetSearch();
  loadBooks();
};

// Setup do Intersection Observer
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