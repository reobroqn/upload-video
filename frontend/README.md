# Blabla Frontend

Modern web interface for the Blabla video platform built with Svelte and Tailwind CSS.

## Features

- ⚡ Svelte for reactive components
- 🎨 Tailwind CSS for utility-first styling
- 🎥 Video player with adaptive streaming
- 🔄 Real-time updates
- 📱 Responsive design
- 🛣️ Client-side routing

## Project Structure

```
frontend/
├── src/
│   ├── assets/        # Static assets
│   ├── components/    # Reusable components
│   ├── routes/        # Page components
│   ├── stores/        # Svelte stores
│   └── App.svelte     # Root component
├── public/            # Public assets
└── index.html         # Entry point
```

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup

1. **Install dependencies**
   ```bash
   npm install
   # or
   yarn
   ```

2. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```
   VITE_API_URL=http://localhost:8000
   ```

## Development

- **Start the development server**:
  ```bash
  npm run dev
  # or
  yarn dev
  ```
  The app will be available at http://localhost:5173

- **Build for production**:
  ```bash
  npm run build
  # or
  yarn build
  ```

## Available Scripts

- `dev`: Start development server
- `build`: Build for production
- `preview`: Preview production build
- `check`: Run type checking
- `check:watch`: Run type checking in watch mode

## Styling

This project uses Tailwind CSS for styling. You can customize the theme in `tailwind.config.js`.
