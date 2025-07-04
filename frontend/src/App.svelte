<script>
  import Layout from './lib/components/Layout.svelte';
  import './app.css';
  
  // This will be replaced with actual routing later
  let currentPage = 'home';
  
  const pages = {
    home: {
      title: 'Welcome to VideoFlow',
      content: 'Upload and manage your videos with ease.'
    }
  };
</script>

<Layout>
  <div class="text-center py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-4">
      {pages[currentPage].title}
    </h1>
    <p class="text-xl text-gray-600 max-w-2xl mx-auto">
      {pages[currentPage].content}
    </p>
    <div class="mt-8">
      <a 
        href="/upload" 
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Upload Video
      </a>
    </div>
  </div>
  
  <div class="bg-white shadow rounded-lg p-6 mt-8">
    <h2 class="text-lg font-medium text-gray-900 mb-4">Recent Videos</h2>
    <div class="text-center py-8 text-gray-500">
      <p>No videos yet. Upload your first video to get started!</p>
    </div>
  </div>
</Layout>
