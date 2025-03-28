import Link from "next/link"
import Image from "next/image"
import { ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen relative overflow-hidden">
      <div className="blob blob-1"></div>
      <div className="blob blob-2"></div>
      <div className="blob blob-3"></div>

      <header className="border-b border-border/40 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div className="container flex h-16 items-center px-4 md:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <div className="w-8 h-8 rounded-md bg-gradient-primary flex items-center justify-center">
              <span className="text-white font-bold">R</span>
            </div>
            <span className="text-indigo-400 font-bold">RoadSense AI</span>
          </Link>
          <nav className="ml-auto flex gap-4 sm:gap-6">
            <Link href="/" className="text-sm font-medium hover:text-indigo-400 transition-colors">
              Home
            </Link>
            <Link href="/what-we-do" className="text-sm font-medium hover:text-indigo-400 transition-colors">
              What We Do
            </Link>
            <Link href="/lets-try" className="text-sm font-medium hover:text-indigo-400 transition-colors">
              Let's Try
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 relative">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none glow-text">
                    <span className="text-indigo-400">Road Anomaly Detection</span> Using Machine Learning
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    Enhancing road safety with advanced AI technology that detects and alerts drivers to potential
                    hazards in real-time.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Link href="/what-we-do">
                    <Button size="lg" className="gap-1 bg-indigo-400 hover:opacity-90 transition-opacity">
                      What We Do
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Link>
                  <Link href="/lets-try">
                    <Button
                      size="lg"
                      variant="outline"
                      className="gap-1 border-primary/50 hover:bg-primary/10 transition-colors"
                    >
                      Let's Try
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </div>
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-primary rounded-2xl opacity-20 blur-xl"></div>
                <Image
                  src="/roadsense.webp"
                  width={550}
                  height={550}
                  alt="Road anomaly detection illustration"
                  className="mx-auto aspect-square overflow-hidden rounded-2xl object-cover sm:w-full lg:order-last relative z-10 glow-border"
                />
              </div>
            </div>
          </div>
        </section>

        <section className="w-full py-12 md:py-24 lg:py-32 bg-muted/30 relative">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-indigo-400">
                  How It Works
                </h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Our advanced machine learning algorithms analyze road conditions in real-time to identify potential
                  hazards.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3 lg:gap-12">
              <div className="flex flex-col justify-center space-y-4 card-hover p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-primary">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-6 w-6"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <path d="M12 16v-4" />
                    <path d="M12 8h.01" />
                  </svg>
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold text-indigo-400">Detect</h3>
                  <p className="text-muted-foreground">
                    Our AI identifies potholes, cracks, and other road anomalies with high precision.
                  </p>
                </div>
              </div>
              <div className="flex flex-col justify-center space-y-4 card-hover p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-secondary">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-6 w-6"
                  >
                    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                    <polyline points="14 2 14 8 20 8" />
                  </svg>
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold text-indigo-400">Analyze</h3>
                  <p className="text-muted-foreground">
                    Process video feeds in real-time to classify and prioritize detected anomalies.
                  </p>
                </div>
              </div>
              <div className="flex flex-col justify-center space-y-4 card-hover p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-accent">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-6 w-6"
                  >
                    <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                  </svg>
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold text-indigo-400">Alert</h3>
                  <p className="text-muted-foreground">
                    Provide timely warnings to drivers and collect data for infrastructure improvement.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-border/40 backdrop-blur-sm bg-background/80">
        <div className="container flex flex-col gap-2 py-4 md:h-16 md:flex-row md:items-center md:py-0">
          <p className="text-xs text-muted-foreground md:text-sm">© 2025 RoadSense AI. All rights reserved.</p>
          <nav className="ml-auto flex gap-4 sm:gap-6">
            <Link href="#" className="text-xs hover:text-primary transition-colors md:text-sm">
              Terms of Service
            </Link>
            <Link href="#" className="text-xs hover:text-primary transition-colors md:text-sm">
              Privacy
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  )
}

