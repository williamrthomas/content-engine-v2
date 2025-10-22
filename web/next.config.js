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
  env: {
    DATABASE_URL: process.env.DATABASE_URL,
  },
  // Enable edge runtime for some API routes
  experimental: {
    serverActions: true,
  },
}

module.exports = nextConfig
