/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: [
      'api.freepik.com',
      'freepik.com',
      // Add your asset domain here
    ],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.freepik.com',
      },
    ],
  },
  // Environment variables are automatically available in API routes
  // No need to explicitly expose them here
  experimental: {
    serverActions: true,
  },
}

module.exports = nextConfig
