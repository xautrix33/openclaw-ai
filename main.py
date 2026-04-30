import logging
import config
import broker
import data_feed
import regime_detector
import signal_engine
import risk_manager
import execution
import journal

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info('Initializing trading bot orchestrator...')

    # Initialize all modules
    config.init()
    broker.init()
    data_feed.init()
    regime_detector.init()
    signal_engine.init()
    risk_manager.init()
    execution.init()
    journal.init()

    try:
        while True:
            logging.info('Running main trading loop...')

            # Regime detection
            regime = regime_detector.detect()
            logging.info(f'Detected regime: {regime}')

            # Signal generation
            signals = signal_engine.generate_signals(regime)
            logging.info(f'Generated signals: {signals}')

            # Signal validation
            valid_signals = signal_engine.validate_signals(signals)
            logging.info(f'Validated signals: {valid_signals}')

            for signal in valid_signals:
                # Risk check before execution
                if risk_manager.check(signal):
                    logging.info(f'Executing signal: {signal}')
                    execution.execute(signal)
                    journal.record(signal)
                else:
                    logging.warning(f'Risk check failed for signal: {signal}')

            # Position management
            broker.manage_positions()

    except Exception as e:
        logging.error(f'Error occurred: {e}', exc_info=True)
    finally:
        logging.info('Shutting down the trading bot orchestrator gracefully...')
        broker.shutdown()

if __name__ == '__main__':
    main()