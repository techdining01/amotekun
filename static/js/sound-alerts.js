/**
 * Sound Alert System
 * Plays different alert sounds based on notification type and report type
 */

class SoundAlerts {
    constructor() {
        // Lazy-load: don't create Audio objects until first user interaction
        this._srcs = {
            chat:     '/static/audio/notification.mp3',
            crime:    '/static/audio/police_siren_sound_effect.mp3',
            violence: '/static/audio/warning.mp3',
            fire:     '/static/audio/emergency_warning_system_united_states.mp3',
            flood:    '/static/audio/emergency_warning_system_united_states.mp3',
            accident: '/static/audio/community_ambulance.mp3',
        };
        this.sounds = {};
        this.enabled = true;
        this.volume = 0.7;
        this.currentlyPlaying = null;
        this._unlocked = false;

        // Unlock audio context on first user gesture
        const unlock = () => {
            if (this._unlocked) return;
            this._unlocked = true;
            // Pre-load all sounds silently
            Object.entries(this._srcs).forEach(([key, src]) => {
                if (!this.sounds[key]) {
                    const a = new Audio(src);
                    a.volume = 0;
                    a.play().then(() => { a.pause(); a.currentTime = 0; a.volume = this.volume; }).catch(() => {});
                    a.addEventListener('ended', () => { if (this.currentlyPlaying === key) this.currentlyPlaying = null; });
                    this.sounds[key] = a;
                }
            });
            ['click','keydown','touchstart','pointerdown'].forEach(e => document.removeEventListener(e, unlock));
        };
        ['click','keydown','touchstart','pointerdown'].forEach(e => document.addEventListener(e, unlock, { once: false, passive: true }));
    }

    _getSound(key) {
        if (!this.sounds[key] && this._srcs[key]) {
            const a = new Audio(this._srcs[key]);
            a.volume = this.volume;
            a.addEventListener('ended', () => { if (this.currentlyPlaying === key) this.currentlyPlaying = null; });
            this.sounds[key] = a;
        }
        return this.sounds[key] || null;
    }
    
    /**
     * Play a specific sound
     * @param {string} soundKey - Key of the sound to play
     * @param {number} volume - Optional volume override (0.0 to 1.0)
     */
    play(soundKey, volume = null) {
        if (!this.enabled) return;
        this.stopAll();
        const sound = this._getSound(soundKey);
        if (!sound) return;
        sound.currentTime = 0;
        sound.volume = volume !== null ? volume : this.volume;
        this.currentlyPlaying = soundKey;
        const p = sound.play();
        if (p && p.catch) p.catch(() => {
            // Autoplay blocked — queue for next interaction
            const retry = () => { sound.play().catch(() => {}); document.removeEventListener('click', retry); };
            document.addEventListener('click', retry, { once: true });
        });
    }
    
    /**
     * Play chat notification sound
     */
    playChat() {
        this.play('chat');
    }
    
    /**
     * Play crime alert sound
     */
    playCrime() {
        this.play('crime');
    }
    
    /**
     * Play violence alert sound
     */
    playViolence() {
        this.play('violence');
    }
    
    /**
     * Play fire alert sound
     */
    playFire() {
        this.play('fire');
    }
    
    /**
     * Play flood alert sound
     */
    playFlood() {
        this.play('flood');
    }
    
    /**
     * Play accident alert sound with high volume
     */
    playAccident() {
        this.play('accident', 1.0); // High volume
    }
    
    /**
     * Play alert based on report type
     * @param {string} reportType - Report type (crime, violence, fire, flood, accident)
     */
    playForReportType(reportType) {
        if (!this.enabled) return;
        
        switch (reportType) {
            case 'crime':
                this.playCrime();
                break;
            case 'violence':
                this.playViolence();
                break;
            case 'fire':
                this.playFire();
                break;
            case 'flood':
                this.playFlood();
                break;
            case 'accident':
                this.playAccident();
                break;
            default:
                this.playChat();
        }
    }
    
    /**
     * Play alert based on notification type
     * @param {Object} notification - Notification object
     */
    playForNotification(notification) {
        if (!this.enabled) return;
        
        switch (notification.notification_type) {
            case 'chat_message':
            case 'operator_communication':
                this.playChat();
                break;
            case 'incident_created':
                // Use report type for incident notifications
                if (notification.data?.report_type) {
                    this.playForReportType(notification.data.report_type);
                } else {
                    this.playChat();
                }
                break;
            case 'dispatch_assigned':
                this.playChat();
                break;
            case 'dispatch_status_changed':
                if (notification.data?.new_status === 'in_progress') {
                    this.play('violence', 0.8);
                }
                break;
            case 'system_alert':
                this.play('fire');
                break;
            default:
                this.playChat();
        }
    }
    
    stopAll() {
        Object.values(this.sounds).forEach(sound => { sound.pause(); sound.currentTime = 0; });
        this.currentlyPlaying = null;
    }

    stop() {
        const sound = this.sounds[this.currentlyPlaying];
        if (sound) { sound.pause(); sound.currentTime = 0; }
        this.currentlyPlaying = null;
    }

    setEnabled(enabled) { this.enabled = enabled; if (!enabled) this.stopAll(); }

    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        Object.values(this.sounds).forEach(s => { s.volume = this.volume; });
    }

    getVolume() { return this.volume; }
    isPlaying() { return this.currentlyPlaying !== null; }
    getCurrentSound() { return this.currentlyPlaying; }
}

// Global instance
const soundAlerts = new SoundAlerts();

if (typeof module !== 'undefined' && module.exports) {
    module.exports = soundAlerts;
}
