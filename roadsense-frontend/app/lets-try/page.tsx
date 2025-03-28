import Link from "next/link"
import { ArrowLeft, Upload, Camera } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function LetsTry() {
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
              <div className="space-y-2 text-center">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl gradient-text glow-text">
                  Let's Try
                </h1>
                <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Experience our road anomaly detection technology in action. Choose one of the options below to get
                  started.
                </p>
              </div>
              <div className="grid gap-6 sm:grid-cols-2">
                <Card className="flex flex-col bg-card/50 backdrop-blur-sm border-primary/20 card-hover">
                  <CardHeader>
                    <CardTitle className="gradient-text">Upload Video</CardTitle>
                    <CardDescription className="text-muted-foreground">
                      Detect road anomalies by uploading a pre-recorded video file.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="flex-1">
                    <div className="flex items-center justify-center py-8">
                      <div className="relative">
                        <div className="absolute inset-0 bg-gradient-primary rounded-full opacity-20 blur-lg"></div>
                        <Upload className="h-16 w-16 text-primary relative z-10" />
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Link href="/lets-try/upload" className="w-full">
                      <Button className="w-full gap-2 bg-gradient-primary hover:opacity-90 transition-opacity">
                        <Upload className="h-4 w-4" />
                        Detect Anomaly by Uploading Video
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
                <Card className="flex flex-col bg-card/50 backdrop-blur-sm border-primary/20 card-hover">
                  <CardHeader>
                    <CardTitle className="gradient-text">Use Camera</CardTitle>
                    <CardDescription className="text-muted-foreground">
                      Detect road anomalies using your webcam, USB camera, or dashcam.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="flex-1">
                    <div className="flex items-center justify-center py-8">
                      <div className="relative">
                        <div className="absolute inset-0 bg-gradient-secondary rounded-full opacity-20 blur-lg"></div>
                        <Camera className="h-16 w-16 text-secondary relative z-10" />
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Link href="/lets-try/camera" className="w-full">
                      <Button className="w-full gap-2 bg-gradient-secondary hover:opacity-90 transition-opacity">
                        <Camera className="h-4 w-4" />
                        Detect Using Camera
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
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

