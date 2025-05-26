library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


-- ============================================================================
entity DLatch is
    port (
        D    : in  std_logic;
        EN   : in  std_logic;
        Q    : out std_logic;
        Qbar : out std_logic
    );
end entity DLatch;
-- ============================================================================

architecture dataflow of DLatch is
    signal Dbar     : std_logic;
    signal R        : std_logic;
    signal S        : std_logic;
    signal Q_int    : std_logic;
    signal Qbar_int : std_logic;
    
begin
    R        <= D nand EN;
    Dbar     <= not D;
    S        <= EN nand Dbar;
    Q_int    <= R nand Qbar_int;
    Q        <= Q_int;
    Qbar_int <= Q_int nand S;
    Qbar     <= Qbar_int;

end dataflow;
    
