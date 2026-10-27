// have i said i dont like javascript?

var map = L.map('map').setView([44.936, 26.018], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	minZoom: 11,
	maxZoom: 15,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	referrerPolicy: true
}).addTo(map);

var busIcon = L.icon({
	iconUrl: './leaflet/images/marker-icon.png',
	iconSize: [45, 45],
});

const markers = new Map();

async function updateMap() {
	try {
		const response = await fetch("/fetch");

		if (!response.ok) {
			throw new Error(`error: ${response.status}`);
		}

		const data = await response.json();

		for (const point of data) {
			const lat = point.position.latitude;
			const lon = point.position.longitude;
			
			const popupContent = `
				<b>${point.numar}</b><br>
				${point.traseu}<br>
				ID: ${point.id}
				`;
			
			if (markers.has(point.id)) {
				const marker = markers.get(point.id);
			
				marker.setLatLng([lat, lon]);
				marker.setPopupContent(popupContent);
			} else {
				const marker = L.marker([lat, lon], {icon: busIcon})
					.addTo(map)
					.bindPopup(popupContent);

				markers.set(point.id, marker);
			}
		}

		console.log("map updated:", new Date().toLocaleTimeString());

	} catch (error) {
		console.error("failed to fetch route data:", error);
	}
}

updateMap();
setInterval(updateMap, 15000);