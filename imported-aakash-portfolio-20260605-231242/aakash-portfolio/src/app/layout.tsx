import type { Metadata } from "next";
import "./globals.css";
import { inter, mono } from "../lib/fonts";
import Navbar from "../components/layout/navbar";
import Footer from "../components/layout/footer";
import ScrollProgress from "../components/layout/scroll-progress";

export const metadata: Metadata = {
  title: "Aakash Nyupane — Creative Technologist",
  description: "Portfolio of Aakash Nyupane — video editor, graphic designer, and creative technologist.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${mono.variable} h-full antialiased`}>
      <body className="min-h-full flex min-h-screen flex-col bg-white text-black dark:bg-black dark:text-white">
        <ScrollProgress />
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
