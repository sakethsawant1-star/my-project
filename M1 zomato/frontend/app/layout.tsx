import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Zomato AI",
  description: "Smart, nuanced dining recommendations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen relative overflow-x-hidden selection:bg-primary/30">
        {/* Subtle background gradients */}
        <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px] pointer-events-none" />
        <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-accent/10 blur-[120px] pointer-events-none" />
        
        <main className="relative z-10 container mx-auto px-4 py-12 max-w-4xl">
          <header className="text-center mb-12 animate-fade-in">
            <h1 className="text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
              Zomato AI
            </h1>
            <p className="text-lg text-slate-400 font-medium">
              Smart, nuanced dining recommendations tailored to your vibe.
            </p>
          </header>
          {children}
        </main>
      </body>
    </html>
  );
}
