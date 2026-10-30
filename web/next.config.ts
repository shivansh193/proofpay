import type { NextConfig } from "next";

// Static export, served by the FastAPI app in production (one Render service).
const config: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
};

export default config;
