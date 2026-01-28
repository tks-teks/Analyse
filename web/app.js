import * as THREE from "https://unpkg.com/three@0.160.0/build/three.module.js";

const canvas = document.getElementById("hologram");
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(window.devicePixelRatio);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  45,
  canvas.clientWidth / canvas.clientHeight,
  0.1,
  100
);
camera.position.set(0, 1.6, 5);

const group = new THREE.Group();
scene.add(group);

const glowMaterial = new THREE.MeshBasicMaterial({
  color: 0x22f1ff,
  wireframe: true,
  transparent: true,
  opacity: 0.6,
});

const coreMaterial = new THREE.MeshStandardMaterial({
  color: 0x071b2e,
  emissive: 0x22f1ff,
  emissiveIntensity: 0.6,
  roughness: 0.3,
  metalness: 0.8,
  transparent: true,
  opacity: 0.85,
});

const torus = new THREE.Mesh(new THREE.TorusKnotGeometry(1, 0.35, 180, 16), coreMaterial);
const wire = new THREE.Mesh(new THREE.TorusKnotGeometry(1.1, 0.4, 120, 12), glowMaterial);

const ring = new THREE.Mesh(
  new THREE.RingGeometry(1.8, 2.05, 64),
  new THREE.MeshBasicMaterial({
    color: 0x22f1ff,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.2,
  })
);
ring.rotation.x = Math.PI / 2;
ring.position.y = -1.1;

const grid = new THREE.GridHelper(6, 30, 0x22f1ff, 0x0a233b);
grid.position.y = -1.5;

const light = new THREE.PointLight(0x22f1ff, 1.2, 10);
light.position.set(2, 3, 4);
scene.add(light, new THREE.AmbientLight(0x0b1e30, 0.6));

const halo = new THREE.Sprite(
  new THREE.SpriteMaterial({
    color: 0x22f1ff,
    opacity: 0.35,
    transparent: true,
  })
);
halo.scale.set(6, 6, 1);

const pulse = new THREE.Mesh(
  new THREE.SphereGeometry(0.1, 32, 32),
  new THREE.MeshBasicMaterial({ color: 0x22f1ff, transparent: true, opacity: 0.8 })
);
pulse.position.set(0.6, 0.5, 1.2);

scene.add(halo);
group.add(torus, wire, ring, grid, pulse);

const feed = document.getElementById("feed");
const timeline = document.getElementById("timeline");
const alerts = [
  { label: "Auth brute-force", level: "Critique" },
  { label: "SQL injection", level: "Élevé" },
  { label: "Exfiltration", level: "Moyen" },
  { label: "Malware", level: "Élevé" },
  { label: "Escalade privilèges", level: "Élevé" },
];

const timelineEvents = [
  { time: "09:12", summary: "Corrélation multi-sources activée" },
  { time: "09:18", summary: "Blocage adaptatif déployé sur 4 sites" },
  { time: "09:21", summary: "Analyse forensique enclenchée" },
  { time: "09:26", summary: "Assistante vocale en mode critique" },
];

function renderFeed() {
  feed.innerHTML = "";
  alerts.slice(0, 4).forEach((alert) => {
    const item = document.createElement("div");
    item.className = "feed-item";
    item.innerHTML = `<span>${alert.label}</span><strong>${alert.level}</strong>`;
    feed.appendChild(item);
  });
}

function renderTimeline() {
  timeline.innerHTML = "";
  timelineEvents.forEach((event) => {
    const item = document.createElement("div");
    item.className = "timeline-item";
    item.innerHTML = `<span>${event.time}</span><strong>${event.summary}</strong>`;
    timeline.appendChild(item);
  });
}

renderFeed();
renderTimeline();

function resize() {
  const { clientWidth, clientHeight } = canvas;
  renderer.setSize(clientWidth, clientHeight, false);
  camera.aspect = clientWidth / clientHeight;
  camera.updateProjectionMatrix();
}

window.addEventListener("resize", resize);
resize();

let time = 0;
function animate() {
  time += 0.01;
  torus.rotation.x += 0.01;
  torus.rotation.y += 0.012;
  wire.rotation.x -= 0.008;
  wire.rotation.y += 0.006;
  ring.rotation.z += 0.002;
  halo.material.opacity = 0.25 + Math.sin(time) * 0.1;
  pulse.material.opacity = 0.6 + Math.sin(time * 2) * 0.2;
  pulse.scale.setScalar(1 + Math.sin(time * 2) * 0.2);
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

animate();

setInterval(() => {
  alerts.unshift(alerts.pop());
  const now = new Date();
  const timestamp = now.toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
  });
  timelineEvents.unshift({
    time: timestamp,
    summary: "Adaptation automatique du score de risque",
  });
  timelineEvents.splice(4);
  renderFeed();
  renderTimeline();
}, 4500);
