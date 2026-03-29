import type { NextConfig } from "next";

// Prevent accidental use of Clerk development keys in production.
// Development keys (pk_test_*) route auth through clerk.accounts.dev and
// expose JWT tokens in URL query parameters, which is a security risk.
if (
  process.env.NODE_ENV === "production" &&
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY?.startsWith("pk_test_")
) {
  throw new Error(
    "Security misconfiguration: a Clerk development key (pk_test_*) is set " +
      "in a production environment. Replace NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY " +
      "and CLERK_SECRET_KEY with your production (pk_live_* / sk_live_*) keys. " +
      "See the Clerk dashboard: https://dashboard.clerk.com"
  );
}

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
