<script>
  import { onMount } from 'svelte';
  import Layout from './lib/components/Layout.svelte';
  import UserProfileForm from './lib/components/UserProfileForm.svelte';
  import VideoUploadForm from './lib/components/VideoUploadForm.svelte';
  import VideoPlayer from './lib/components/VideoPlayer.svelte'; // Import VideoPlayer
  import { videos } from './lib/stores/videos'; // Import the videos store
  import './app.css';
  
  let currentPage = 'home';
  let showProfileForm = false;
  let showUploadForm = false; // New state for upload form visibility
  let user = {};

  const pages = {
    home: {
      title: 'Welcome to VideoFlow',
      content: 'Upload and manage your videos with ease.'
    }
  };

  async function fetchUserProfile() {
    try {
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

  async function fetchVideos() {
    try {
      const response = await fetch('http://localhost:8000/api/v1/videos/', {
        headers: {
          'Authorization': `Bearer YOUR_JWT_TOKEN` // Replace with actual token
        }
      });
      if (response.ok) {
        const data = await response.json();
        videos.set(data);
      } else {
        console.error('Failed to fetch videos:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching videos:', error);
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

  async function handleUploadVideo(event) {
    const { title, description, file } = event.detail;

    try {
      // 1. Request presigned URL from backend
      const requestBody = {
        title: title,
        description: description,
        file_name: file.name,
        file_size: file.size,
        mime_type: file.type,
      };

      const presignedResponse = await fetch('http://localhost:8000/api/v1/videos/upload-request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer YOUR_JWT_TOKEN` // Replace with actual token
        },
        body: JSON.stringify(requestBody),
      });

      if (!presignedResponse.ok) {
        const errorData = await presignedResponse.json();
        throw new Error(errorData.detail || 'Failed to get presigned URL');
      }

      const { url, fields, video_id } = await presignedResponse.json();

      // 2. Upload file directly to S3 using the presigned URL
      const formData = new FormData();
      for (const key in fields) {
        formData.append(key, fields[key]);
      }
      formData.append('file', file); // The file must be the last field

      const uploadResponse = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error('Failed to upload file to S3');
      }

      // 3. Confirm upload completion with backend
      const confirmResponse = await fetch('http://localhost:8000/api/v1/videos/upload-complete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer YOUR_JWT_TOKEN` // Replace with actual token
        },
        body: JSON.stringify({ video_id: video_id }),
      });

      if (!confirmResponse.ok) {
        const errorData = await confirmResponse.json();
        throw new Error(errorData.detail || 'Failed to confirm upload completion');
      }

      alert('Video uploaded successfully!');
      showUploadForm = false; // Hide form after successful upload
      fetchVideos(); // Refresh video list after successful upload

    } catch (error) {
      console.error('Error during video upload:', error);
      alert(`Video upload failed: ${error.message}`);
    }
  }

  // Fetch user profile and videos on component mount
  onMount(() => {
    fetchUserProfile();
    fetchVideos();
  });
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
      <button
        on:click={() => showUploadForm = !showUploadForm}
        class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        {showUploadForm ? 'Hide Upload Form' : 'Upload Video'}
      </button>
      <button
        on:click={() => showProfileForm = !showProfileForm}
        class="ml-4 inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-blue-600 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        {showProfileForm ? 'Hide Profile Form' : 'Edit Profile'}
      </button>
    </div>
  </div>
  
  {#if showUploadForm}
    <div class="bg-white shadow rounded-lg p-6 mt-8">
      <h2 class="text-lg font-medium text-gray-900 mb-4">Upload New Video</h2>
      <VideoUploadForm on:uploadVideo={handleUploadVideo} />
    </div>
  {/if}

  {#if showProfileForm}
    <div class="bg-white shadow rounded-lg p-6 mt-8">
      <h2 class="text-lg font-medium text-gray-900 mb-4">Edit User Profile</h2>
      <UserProfileForm user={user} on:updateProfile={handleUpdateProfile} />
    </div>
  {/if}

  <div class="bg-white shadow rounded-lg p-6 mt-8">
    <h2 class="text-lg font-medium text-gray-900 mb-4">Recent Videos</h2>
    {#if $videos.length > 0}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each $videos as video (video.id)}
          <div class="border rounded-lg overflow-hidden shadow-sm">
            <VideoPlayer
              options={{
                controls: true,
                responsive: true,
                fluid: true,
              }}
              src={`http://localhost:9000/${video.file_key}`}
              type={video.mime_type}
            />
            <div class="p-4">
              <h3 class="text-lg font-semibold">{video.title}</h3>
              <p class="text-gray-600 text-sm">{video.description}</p>
            </div>
          </div>
        {/each}
      </div>
    {:else}
      <div class="text-center py-8 text-gray-500">
        <p>No videos yet. Upload your first video to get started!</p>
      </div>
    {/if}
  </div>
</Layout>
