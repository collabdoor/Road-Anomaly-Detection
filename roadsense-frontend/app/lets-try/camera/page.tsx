"use client"

import { useState, useRef, useEffect } from "react"
import Link from "next/link"
import { ArrowLeft, Camera, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function CameraDetection() {
  const [isStreaming, setIsStreaming] = useState(false)
  const [devices, setDevices] = useState<MediaDeviceInfo[]>([])
  const [selectedDevice, setSelectedDevice] = useState<string>("")
  const [detections, setDetections] = useState<Array<{ type: string; confidence: number; timestamp: string }>>([])
  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)

  useEffect(() => {
    // Get available video devices
    async function getDevices() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices()
        const videoDevices = devices.filter((device) => device.kind === "videoinput")
        setDevices(videoDevices)
        if (videoDevices.length > 0) {
          setSelectedDevice(videoDevices[0].deviceId)
        }
      } catch (err) {
        console.error("Error accessing media devices:", err)
      }
    }

    getDevices()

    return () => {
      // Clean up stream when component unmounts
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop())
      }
    }
  }, [])

  const startStream = async () => {
    try {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop())
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          deviceId: selectedDevice ? { exact: selectedDevice } : undefined,
        },
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
        streamRef.current = stream
        setIsStreaming(true)

        // Start simulated detection
        startDetection()
      }
    } catch (err) {
      console.error("Error starting stream:", err)
    }
  }

  const stopStream = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
      if (videoRef.current) {
        videoRef.current.srcObject = null
      }
      setIsStreaming(false)
      setDetections([])
    }
  }

  const startDetection = () => {
    // Simulate random detections
    const detectionInterval = setInterval(() => {
      if (!isStreaming) {
        clearInterval(detectionInterval)
        return
      }

      // Random chance to detect an anomaly
      if (Math.random() > 0.7) {
        const anomalyTypes = ["Pothole", "Crack", "Debris", "Water Puddle"]
        const randomType = anomalyTypes[Math.floor(Math.random() * anomalyTypes.length)]
        const randomConfidence = Math.floor(Math.random() * 30) + 70 // 70-99%
        const now = new Date()

        setDetections((prev) => [
          {
            type: randomType,
            confidence: randomConfidence,
            timestamp: now.toLocaleTimeString(),
          },
          ...prev.slice(0, 4), // Keep only the 5 most recent detections
        ])
      }
    }, 3000)

    return () => clearInterval(detectionInterval)
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
                  Camera Detection
                </h1>
                <p className="text-muted-foreground">
                  Use your webcam, USB camera, or dashcam to detect road anomalies in real-time.
                </p>
              </div>

              <div className="space-y-8">
                <div className="space-y-4 p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="w-full sm:w-2/3">
                      <label className="text-sm font-medium gradient-text">Select Camera</label>
                      <Select value={selectedDevice} onValueChange={setSelectedDevice} disabled={isStreaming}>
                        <SelectTrigger className="w-full bg-muted/30 border-primary/20">
                          <SelectValue placeholder="Select a camera" />
                        </SelectTrigger>
                        <SelectContent className="bg-card border-primary/20">
                          {devices.map((device) => (
                            <SelectItem key={device.deviceId} value={device.deviceId}>
                              {device.label || `Camera ${devices.indexOf(device) + 1}`}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="flex items-end">
                      {!isStreaming ? (
                        <Button
                          onClick={startStream}
                          disabled={!selectedDevice}
                          className="gap-2 bg-gradient-secondary hover:opacity-90 transition-opacity"
                        >
                          <Camera className="h-4 w-4" />
                          Start Detection
                        </Button>
                      ) : (
                        <Button
                          onClick={stopStream}
                          variant="destructive"
                          className="bg-gradient-accent hover:opacity-90 transition-opacity"
                        >
                          Stop Detection
                        </Button>
                      )}
                    </div>
                  </div>

                  <div className="aspect-video bg-black rounded-xl overflow-hidden relative">
                    <div className="absolute inset-0 bg-gradient-secondary opacity-10"></div>
                    <video ref={videoRef} className="w-full h-full relative z-10" autoPlay playsInline muted />
                    {!isStreaming && (
                      <div className="absolute inset-0 flex items-center justify-center bg-black/50 text-white backdrop-blur-sm">
                        <div className="text-center">
                          <div className="relative mx-auto mb-2">
                            <div className="absolute inset-0 bg-gradient-secondary rounded-full opacity-20 blur-lg"></div>
                            <Camera className="h-12 w-12 mx-auto relative z-10 text-secondary" />
                          </div>
                          <p className="gradient-text">Camera feed will appear here</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div className="space-y-4 p-6 rounded-xl bg-card/50 backdrop-blur-sm">
                  <h3 className="text-lg font-medium gradient-text">Live Detections</h3>
                  {detections.length > 0 ? (
                    <div className="space-y-2">
                      {detections.map((detection, index) => (
                        <Alert
                          key={index}
                          variant={index === 0 ? "destructive" : "default"}
                          className="bg-muted/30 backdrop-blur-sm border-primary/20"
                        >
                          <AlertTriangle className="h-4 w-4" />
                          <AlertTitle className={index === 0 ? "text-destructive" : "gradient-text"}>
                            {detection.type} Detected
                          </AlertTitle>
                          <AlertDescription>
                            Confidence: {detection.confidence}% | Time: {detection.timestamp}
                          </AlertDescription>
                        </Alert>
                      ))}
                    </div>
                  ) : (
                    <p className="text-muted-foreground text-sm">
                      {isStreaming
                        ? "Monitoring for road anomalies. Detections will appear here."
                        : "Start the camera to begin detecting road anomalies."}
                    </p>
                  )}
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

