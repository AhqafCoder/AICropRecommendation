import { SignUp } from '@clerk/nextjs';

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Join CropAI</h1>
          <p className="text-gray-600">Create your account to get started</p>
        </div>
        <SignUp 
          appearance={{
            elements: {
              formButtonPrimary: 'bg-green-600 hover:bg-green-700 text-sm normal-case',
              card: 'shadow-xl',
              headerTitle: 'hidden',
              headerSubtitle: 'hidden',
            }
          }}
        />
      </div>
    </div>
  );
}