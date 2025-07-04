<script>
  export let title = 'VideoFlow';
  
  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Upload', href: '/upload' },
    { name: 'Videos', href: '/videos' },
  ];
</script>

<nav class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <div class="flex items-center">
        <a href="/" class="text-xl font-bold text-gray-900">VideoFlow</a>
      </div>
      <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
        {#each navItems as item}
          <a 
            href={item.href}
            class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
          >
            {item.name}
          </a>
        {/each}
      </div>
    </div>
  </div>
</nav>

<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <slot />
</main>

<footer class="bg-white border-t mt-8 py-4">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
    &copy; 2025 VideoFlow. All rights reserved.
  </div>
</footer>
