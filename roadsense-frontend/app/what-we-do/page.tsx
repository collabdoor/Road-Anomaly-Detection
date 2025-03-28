import Link from "next/link"
import Image from "next/image"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function WhatWeDo() {
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
            <span className="gradient-text font-bold">RoadSense AI</span>
          </Link>
          <nav className="ml-auto flex gap-4 sm:gap-6">
            <Link href="/" className="text-sm font-medium hover:text-primary transition-colors">
              Home
            </Link>
            <Link href="/what-we-do" className="text-sm font-medium hover:text-primary transition-colors">
              What We Do
            </Link>
            <Link href="/lets-try" className="text-sm font-medium hover:text-primary transition-colors">
              Let's Try
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container px-4 md:px-6">
            <div className="mx-auto max-w-3xl space-y-6">
              <Link href="/">
                <Button variant="ghost" size="sm" className="gap-1 hover:bg-primary/10 transition-colors">
                  <ArrowLeft className="h-4 w-4" />
                  Back to Home
                </Button>
              </Link>
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl gradient-text glow-text">
                  What We Do
                </h1>
                <p className="text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Our mission is to improve road safety through advanced machine learning technology.
                </p>
              </div>
              <div className="space-y-8">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-primary rounded-2xl opacity-20 blur-xl"></div>
                  <Image
                    src="/whatwedo.jpg"
                    width={800}
                    height={400}
                    alt="Road anomaly detection system in action"
                    className="aspect-video overflow-hidden rounded-2xl object-cover relative z-10 glow-border"
                  />
                </div>
                <div className="space-y-4 p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                  <h2 className="text-2xl font-bold gradient-text">The Problem</h2>
                  <p className="text-muted-foreground md:text-lg/relaxed">
                    Road anomalies such as potholes, cracks, and debris cause accidents, vehicle damage, and traffic
                    disruptions worldwide. Traditional detection methods are slow, labor-intensive, and often reactive
                    rather than preventive.
                  </p>
                </div>
                <div className="space-y-4 p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                  <h2 className="text-2xl font-bold gradient-text">Our Solution</h2>
                  <p className="text-muted-foreground md:text-lg/relaxed">
                    RoadSense AI uses computer vision and machine learning algorithms to automatically detect and
                    classify road anomalies in real-time. Our technology can be integrated with dashcams, traffic
                    cameras, or specialized vehicle-mounted systems.
                  </p>
                </div>
                <div className="space-y-4 p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                  <h2 className="text-2xl font-bold gradient-text">Key Features</h2>
                  <ul className="list-disc list-inside space-y-2 text-muted-foreground md:text-lg/relaxed pl-4">
                    <li>Real-time detection of potholes, cracks, and other road hazards</li>
                    <li>High accuracy classification of anomaly types and severity</li>
                    <li>Works in various lighting and weather conditions</li>
                    <li>Integrates with existing camera systems</li>
                    <li>Generates detailed reports for infrastructure maintenance</li>
                    <li>Driver alert system for immediate hazard awareness</li>
                  </ul>
                </div>
                <div className="space-y-4 p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                  <h2 className="text-2xl font-bold gradient-text">Applications</h2>
                  <div className="grid gap-6 sm:grid-cols-2">
                    <div className="flex flex-col space-y-2 p-4 rounded-lg bg-muted/30 card-hover">
                      <h3 className="font-bold gradient-text">Individual Drivers</h3>
                      <p className="text-sm text-muted-foreground">
                        Get real-time alerts about road hazards to avoid vehicle damage and improve safety.
                      </p>
                    </div>
                    <div className="flex flex-col space-y-2 p-4 rounded-lg bg-muted/30 card-hover">
                      <h3 className="font-bold gradient-text">Fleet Management</h3>
                      <p className="text-sm text-muted-foreground">
                        Optimize routes and reduce maintenance costs by avoiding roads with detected anomalies.
                      </p>
                    </div>
                    <div className="flex flex-col space-y-2 p-4 rounded-lg bg-muted/30 card-hover">
                      <h3 className="font-bold gradient-text">City Governments</h3>
                      <p className="text-sm text-muted-foreground">
                        Prioritize road repairs based on data-driven insights about anomaly locations and severity.
                      </p>
                    </div>
                    <div className="flex flex-col space-y-2 p-4 rounded-lg bg-muted/30 card-hover">
                      <h3 className="font-bold gradient-text">Research Institutions</h3>
                      <p className="text-sm text-muted-foreground">
                        Collect and analyze road condition data for infrastructure studies and improvements.
                      </p>
                    </div>
                  </div>
                </div>
                <div className="flex justify-center">
                  <Link href="/lets-try">
                    <Button size="lg" className="gap-1 bg-gradient-primary hover:opacity-90 transition-opacity">
                      Try Our Technology
                      <ArrowLeft className="h-4 w-4 rotate-180" />
                    </Button>
                  </Link>
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

