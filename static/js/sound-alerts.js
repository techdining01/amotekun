/**
 * Sound Alert System
 * Plays different alert sounds based on notification type and report type
 */

class SoundAlerts {
    constructor() {
        this.sounds = {
            chat: new Audio('/static/audio/notification.mp3'),
            crime: new Audio('/static/audio/police_siren_sound_effect.mp3'),
            violence: new Audio('/static/audio/warning.mp3'),
            fire: new Audio('/static/audio/emergency_warning_system_united_states.mp3'),
            flood: new Audio('/static/audio/emergency_warning_system_united_states.mp3'),
            accident: new Audio('/static/audio/community_ambulance.mp3'),
        };
        
        this.enabled = true;
        this.volume = 0.5;
        this.currentlyPlaying = null;
        
        // Set initial volume
        Object.values(this.sounds).forEach(sound => {
            sound.volume = this.volume;
        });
        
        // Track when sounds end
        Object.entries(this.sounds).forEach(([key, sound]) => {
            sound.addEventListener('ended', () => {
                if (this.currentlyPlaying === key) {
                    this.currentlyPlaying = null;
                }
            });
        });
    }
    
    /**
     * Play a specific sound
     * @param {string} soundKey - Key of the sound to play
     * @param {number} volume - Optional volume override (0.0 to 1.0)
     */
    play(soundKey, volume = null) {
        if (!this.enabled || !this.sounds[soundKey]) return;
        
        // Stop currently playing sound
        this.stopAll();
        
        const sound = this.sounds[soundKey];
        sound.currentTime = 0;
        sound.volume = volume !== null ? volume : this.volume;
        this.currentlyPlaying = soundKey;
        
        sound.play().catch(e => console.log('Audio play failed:', e));
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
    
    /**
     * Stop all playing sounds
     */
    stopAll() {
        Object.values(this.sounds).forEach(sound => {
            sound.pause();
            sound.currentTime = 0;
        });
        this.currentlyPlaying = null;
    }
    
    /**
     * Stop currently playing sound
     */
    stop() {
        if (this.currentlyPlaying && this.sounds[this.currentlyPlaying]) {
            const sound = this.sounds[this.currentlyPlaying];
            sound.pause();
            sound.currentTime = 0;
            this.currentlyPlaying = null;
        }
    }
    
    /**
     * Pause currently playing sound (can be resumed)
     */
    pause() {
        if (this.currentlyPlaying && this.sounds[this.currentlyPlaying]) {
            this.sounds[this.currentlyPlaying].pause();
        }
    }
    
    /**
     * Resume paused sound
     */
    resume() {
        if (this.currentlyPlaying && this.sounds[this.currentlyPlaying]) {
            this.sounds[this.currentlyPlaying].play()
                .catch(e => console.log('Audio resume failed:', e));
        }
    }
    
    /**
     * Check if a sound is currently playing
     * @returns {boolean}
     */
    isPlaying() {
        return this.currentlyPlaying !== null;
    }
    
    /**
     * Get currently playing sound key
     * @returns {string|null}
     */
    getCurrentSound() {
        return this.currentlyPlaying;
    }
    
    /**
     * Enable or disable sound alerts
     * @param {boolean} enabled
     */
    setEnabled(enabled) {
        this.enabled = enabled;
        if (!enabled) {
            this.stopAll();
        }
    }
    
    /**
     * Set master volume
     * @param {number} volume - 0.0 to 1.0
     */
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        Object.values(this.sounds).forEach(sound => {
            sound.volume = this.volume;
        });
    }
    
    /**
     * Get current volume
     * @returns {number}
     */
    getVolume() {
        return this.volume;
    }
}

// Global instance
const soundAlerts = new SoundAlerts();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = soundAlerts;
}
