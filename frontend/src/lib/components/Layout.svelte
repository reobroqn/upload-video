<script>
  export let title = 'VideoFlow';
  let mobileMenuOpen = false; // State for mobile menu
  
  const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Upload', href: '/upload' },
    { name: 'Videos', href: '/videos' },
  ];

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }
</script>

<nav class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <div class="flex items-center">
        <a href="/" class="text-xl font-bold text-gray-900">VideoFlow</a>
      </div>
      <div class="-mr-2 flex items-center sm:hidden"> <!-- Mobile menu button -->
        <button type="button" on:click={toggleMobileMenu} class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500" aria-controls="mobile-menu" aria-expanded="false">
          <span class="sr-only">Open main menu</span>
          {#if mobileMenuOpen}
            <!-- Icon when menu is open -->
            <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          {:else}
            <!-- Icon when menu is closed -->
            <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          {/if}
        </button>
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

  <!-- Mobile menu, show/hide based on menu state. -->
  {#if mobileMenuOpen}
    <div class="sm:hidden" id="mobile-menu">
      <div class="pt-2 pb-3 space-y-1">
        {#each navItems as item}
          <a href={item.href} class="block pl-3 pr-4 py-2 border-l-4 border-blue-500 text-base font-medium text-blue-700">
            {item.name}
          </a>
        {/each}
      </div>
    </div>
  {/if}

<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
  <slot />
</main>

<footer class="bg-white border-t mt-8 py-4">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
    &copy; 2025 VideoFlow. All rights reserved.
  </div>
</footer>
