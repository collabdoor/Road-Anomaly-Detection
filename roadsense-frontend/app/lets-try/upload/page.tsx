"use client"

import type React from "react"

import { useState, useRef } from "react"
import Link from "next/link"
import { ArrowLeft, Upload, Play, Pause, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function UploadVideo() {
  const [file, setFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [detections, setDetections] = useState<Array<{ type: string; confidence: number; timestamp: number }>>([])
  const videoRef = useRef<HTMLVideoElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setDetections([])
      setProgress(0)
      setIsProcessing(false)
    }
  }

  const handleProcessVideo = () => {
    if (!file) return

    setIsProcessing(true)

    // Simulate processing with progress updates
    let currentProgress = 0
    const interval = setInterval(() => {
      currentProgress += 5
      setProgress(currentProgress)

      // Simulate random detections
      if (currentProgress % 20 === 0) {
        const anomalyTypes = ["Pothole", "Crack", "Debris", "Water Puddle"]
        const randomType = anomalyTypes[Math.floor(Math.random() * anomalyTypes.length)]
        const randomConfidence = Math.floor(Math.random() * 30) + 70 // 70-99%
        const timestamp = (currentProgress / 100) * (videoRef.current?.duration || 60)

        setDetections((prev) => [
          ...prev,
          {
            type: randomType,
            confidence: randomConfidence,
            timestamp,
          },
        ])
      }

      if (currentProgress >= 100) {
        clearInterval(interval)
        setIsProcessing(false)
      }
    }, 200)
  }

  const togglePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

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
        <section className="w-full py-12 md:py-24">
          <div className="container px-4 md:px-6">
            <div className="mx-auto max-w-4xl space-y-6">
              <Link href="/lets-try">
                <Button variant="ghost" size="sm" className="gap-1 hover:bg-primary/10 transition-colors">
                  <ArrowLeft className="h-4 w-4" />
                  Back to Options
                </Button>
              </Link>
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl gradient-text glow-text">
                  Upload Video
                </h1>
                <p className="text-muted-foreground">
                  Upload a video of a road to detect anomalies such as potholes, cracks, and other hazards.
                </p>
              </div>

              <div className="space-y-8">
                <div className="flex flex-col items-center justify-center border-2 border-dashed border-primary/25 rounded-lg p-12 text-center bg-card/30 backdrop-blur-sm">
                  <div className="space-y-2">
                    <div className="relative">
                      <div className="absolute inset-0 bg-gradient-primary rounded-full opacity-20 blur-lg"></div>
                      <Upload className="h-8 w-8 mx-auto text-primary relative z-10" />
                    </div>
                    <h3 className="font-medium gradient-text">Upload your video</h3>
                    <p className="text-xs text-muted-foreground">Supported formats: MP4, AVI, MOV (max 100MB)</p>
                  </div>
                  <label className="mt-4">
                    <Button variant="outline" className="mt-2 border-primary/50 hover:bg-primary/10 transition-colors">
                      Select File
                    </Button>
                    <input
                      type="file"
                      className="sr-only"
                      accept="video/mp4,video/avi,video/quicktime"
                      onChange={handleFileChange}
                    />
                  </label>
                  {file && <p className="mt-2 text-sm text-primary">{file.name}</p>}
                </div>

                {file && (
                  <div className="space-y-4">
                    <div className="aspect-video bg-black rounded-xl overflow-hidden relative">
                      <div className="absolute inset-0 bg-gradient-primary opacity-10"></div>
                      <video
                        ref={videoRef}
                        src={URL.createObjectURL(file)}
                        className="w-full h-full relative z-10"
                        controls={false}
                        onPlay={() => setIsPlaying(true)}
                        onPause={() => setIsPlaying(false)}
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={togglePlayPause}
                        className="border-primary/50 hover:bg-primary/10 transition-colors"
                      >
                        {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                      </Button>

                      <Button
                        onClick={handleProcessVideo}
                        disabled={isProcessing}
                        className="bg-gradient-primary hover:opacity-90 transition-opacity"
                      >
                        {isProcessing ? "Processing..." : "Detect Anomalies"}
                      </Button>
                    </div>

                    {isProcessing && (
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span>Processing video</span>
                          <span className="text-primary">{progress}%</span>
                        </div>
                        <Progress value={progress} className="h-2 bg-muted/50">
                          <div
                            className="h-full bg-gradient-primary rounded-full animated-gradient"
                            style={{ width: `${progress}%` }}
                          />
                        </Progress>
                      </div>
                    )}

                    {detections.length > 0 && (
                      <div className="space-y-4">
                        <h3 className="text-lg font-medium gradient-text">Detected Anomalies</h3>
                        <div className="space-y-2">
                          {detections.map((detection, index) => (
                            <Alert
                              key={index}
                              variant={index === 0 ? "destructive" : "default"}
                              className="bg-card/50 backdrop-blur-sm border-primary/20"
                            >
                              <AlertTriangle className="h-4 w-4" />
                              <AlertTitle className={index === 0 ? "text-destructive" : "gradient-text"}>
                                {detection.type} Detected
                              </AlertTitle>
                              <AlertDescription>
                                Confidence: {detection.confidence}% | Timestamp: {formatTime(detection.timestamp)}
                              </AlertDescription>
                            </Alert>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
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

