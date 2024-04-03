import styles from './Header.module.css'


const Header: React.FC = () => {
  return(
    <div>
      <header className={styles.header}>
        <h1>CoinSage</h1>
      </header>
    </div>
  );
}

export default Header;