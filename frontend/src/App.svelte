<script>
  import Layout from './lib/components/Layout.svelte';
  import UserProfileForm from './lib/components/UserProfileForm.svelte';
  import './app.css';
  
  let currentPage = 'home';
  let showProfileForm = false;
  let user = {};

  const pages = {
    home: {
      title: 'Welcome to VideoFlow',
      content: 'Upload and manage your videos with ease.'
    }
  };

  async function fetchUserProfile() {
    try {
      // Replace with your actual API endpoint and authentication logic
      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        headers: {
          'Authorization': `Bearer YOUR_JWT_TOKEN` // Replace with actual token
        }
      });
      if (response.ok) {
        user = await response.json();
      } else {
        console.error('Failed to fetch user profile:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  }

  async function handleUpdateProfile(event) {
    const updatedData = event.detail;
    try {
      const response = await fetch('http://localhost:8000/api/v1/users/me', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer YOUR_JWT_TOKEN` // Replace with actual token
        },
        body: JSON.stringify(updatedData)
      });
      if (response.ok) {
        user = await response.json();
        showProfileForm = false; // Hide form after successful update
        alert('Profile updated successfully!');
      } else {
        console.error('Failed to update user profile:', response.statusText);
        alert('Failed to update profile.');
      }
    } catch (error) {
      console.error('Error updating user profile:', error);
      alert('Error updating profile.');
    }
  }

  // Fetch user profile on component mount
  fetchUserProfile();
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
      <button
        on:click={() => showProfileForm = !showProfileForm}
        class="ml-4 inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-blue-600 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        {showProfileForm ? 'Hide Profile Form' : 'Edit Profile'}
      </button>
    </div>
  </div>
  
  {#if showProfileForm}
    <div class="bg-white shadow rounded-lg p-6 mt-8">
      <h2 class="text-lg font-medium text-gray-900 mb-4">Edit User Profile</h2>
      <UserProfileForm user={user} on:updateProfile={handleUpdateProfile} />
    </div>
  {/if}

  <div class="bg-white shadow rounded-lg p-6 mt-8">
    <h2 class="text-lg font-medium text-gray-900 mb-4">Recent Videos</h2>
    <div class="text-center py-8 text-gray-500">
      <p>No videos yet. Upload your first video to get started!</p>
    </div>
  </div>
</Layout>
