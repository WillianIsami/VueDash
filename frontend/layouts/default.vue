<template>
  <div>
    <header>
      <nav>
        <ul>
          <li><NuxtLink to="/" class="nav-link">Home</NuxtLink></li>
          <li><NuxtLink to="/books" class="nav-link">Books</NuxtLink></li>
          <li><NuxtLink to="/popular" class="nav-link">Popular Books</NuxtLink></li>
        </ul>
      </nav>
    </header>

    <main>
      <slot />
    </main>
  </div>
</template>

<script setup></script>

<style scoped>
header {
  background-color: #0d78b6;
  padding: 10px 20px;
}

nav ul {
  display: flex;
  justify-content: space-around;
  list-style: none;
  padding: 0;
  margin: 0;
}

nav li {
  margin: 0 15px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 18px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #3498db;
  color: white;
}

@media (max-width: 768px) {
  nav ul {
    flex-direction: column;
    align-items: center;
  }
  nav li {
    margin: 10px 0;
  }
}
</style>
